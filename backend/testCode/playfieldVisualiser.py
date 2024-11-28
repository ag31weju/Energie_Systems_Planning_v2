import os
import pygame
from xml_to_json_map import load_element_map

# Playfield config
GRID_SIZE = 60  # Size of each grid cell (pixels)
WINDOW_WIDTH = 800  # Window width (pixels)
WINDOW_HEIGHT = 600  # Window height (pixels)
IMAGE_FOLDER = "images"  # Folder containing images

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Element Map Viewer")
clock = pygame.time.Clock()

# Load element map
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, "json", "element_map.json")
element_map = load_element_map(json_file_path)

# Load images into a dictionary
images = {}
for element_type in set(element_map.values()):
    image_path = os.path.join(current_directory, IMAGE_FOLDER, f"{element_type}.png")
    if os.path.exists(image_path):
        images[element_type] = pygame.image.load(image_path)
    else:
        print(f"Warning: Image for '{element_type}' not found at {image_path}")


# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((255, 255, 255))  # White background

    # Draw elements
    for coord, element_type in element_map.items():
        x, y = map(int, coord.split(","))
        if element_type in images:
            # Get the image and scale it to the grid size
            image = pygame.transform.scale(images[element_type], (GRID_SIZE, GRID_SIZE))
            # Calculate the position
            pos_x, pos_y = x * GRID_SIZE, y * GRID_SIZE
            # Blit the image onto the screen
            screen.blit(image, (pos_x, pos_y))

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 frames per second

pygame.quit()
