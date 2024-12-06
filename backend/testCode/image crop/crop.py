import os
from PIL import Image

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to the image in the same folder as the script
image_path = os.path.join(script_directory, "img2.png")

# Check if the file exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image not found at: {image_path}")

# Open the image
image = Image.open(image_path)

# Get the original image dimensions
image_width, image_height = image.size

# Determine the size of the square (smallest dimension)
square_size = min(image_width, image_height)

# Calculate the coordinates for the cropping box (centered square)
left = (image_width - square_size) // 2
top = (image_height - square_size) // 2
right = left + square_size
bottom = top + square_size

# Perform the cropping to create a square image
square_image = image.crop((left, top, right, bottom))

# Optionally resize the square to a fixed dimension (e.g., 200x200)
target_size = (2000, 2000)  # Change this to your desired HTML display size
resized_square_image = square_image.resize(target_size, Image.Resampling.LANCZOS)

# Save the resized square image
resized_square_image.save(os.path.join(script_directory, "square_image2.png"))  # Save the final square image
resized_square_image.show()  # Open the resized square image for preview

print(f"Square image saved as 'square_image.png' with dimensions: {target_size[0]}x{target_size[1]}")
