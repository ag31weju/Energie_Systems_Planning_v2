import json
from PIL import Image
import io
from pathlib import Path
from graph_to_scenario.create_scenario import Scenario

"""
This does image and JSON processing of the Scenario uploaded by the user.
Image is cropped and Json file is parsed and printed out(just for testing)

"""

def process_image(image_file):
    try:
        # Open the image using Pillow
        img = Image.open(image_file)

        # Get the original image dimensions
        img_width, img_height = img.size

        # Determine the size of the square (smallest dimension)
        square_size = min(img_width, img_height)

        # Calculate the coordinates for the cropping box (centered square)
        left = (img_width - square_size) // 2
        top = (img_height - square_size) // 2
        right = left + square_size
        bottom = top + square_size

        # Perform the cropping to create a square image
        square_image = img.crop((left, top, right, bottom))

        # Resize the cropped image to 2000x2000 pixels
        target_size = (2000, 2000)
        resized_square_image = square_image.resize(
            target_size, Image.Resampling.LANCZOS
        )

        # Save the processed image to an in-memory file
        img_io = io.BytesIO()
        resized_square_image.save(img_io, format="PNG")
        img_io.seek(0)

        return img_io
    except Exception as e:
        raise RuntimeError(f"Error processing image: {str(e)}")


def parse_json(json_file):
    '''
    Get the json file from frontend and using create_scenario.py, parse the json file for optimizer
    '''
    ''' commented out for now, fix node labels in frontend first
    try:
        # Read and decode the JSON file
        json_data = json_file.read().decode("utf-8")
        parsed_data = json.loads(json_data)
        current_dir = Path(__file__).parent #current directory
        default_value_file = current_dir.parent/ "graph_to_scenario" / "default_node_values.json" #default values json file
        scenario = Scenario(parsed_data, None, default_value_file) #create a scenario object

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error parsing JSON file: {str(e)}")
    '''


'''
How to Navigate to a File in a Sibling Folder Using pathlib
    -Import Path from pathlib.
    -Use Path(__file__).parent to get the current script's directory.
    -Use .parent on the current directory to move up one level (equivalent to cd.. in terminal).
    -Combine the parent directory with the sibling folder name and file name using / (e.g., parent_dir / "folder_name" / "file_name.json").
    -Use .exists() to check if the file exists before opening or processing it.
    -Open and process the file if it exists; otherwise, handle the case where it does not.
'''