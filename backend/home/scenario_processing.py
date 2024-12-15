import json
from PIL import Image
import io

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
    try:
        # Read and decode the JSON file
        json_data = json_file.read().decode("utf-8")
        parsed_data = json.loads(json_data)

        # Print parsed content
        print("Nodes:")
        for node in parsed_data.get("nodes", []):
            print(
                f"  ID: {node['id']}, Type: {node['type']}, Name: {node['name']}, Position: ({node['x']}, {node['y']})"
            )

        print("Edges:")
        for edge in parsed_data.get("edges", []):
            print(
                f"  Start: {edge['start']}, End: {edge['end']}, Weight: {edge['weight']}"
            )

        return parsed_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error parsing JSON file: {str(e)}")
