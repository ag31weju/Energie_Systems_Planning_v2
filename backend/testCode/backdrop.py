import pygame
import os
import tkinter as tk
from tkinter import simpledialog

# Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 50
BACKGROUND_IMAGE = "background2.png"
IMAGE_TO_ADD = "marker.png"  # The image to be placed on the grid
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 150, 255)
TEXT_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Add Image to Grid")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Load the background image
current_directory = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_directory, BACKGROUND_IMAGE)
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the marker image
marker_image_path = os.path.join(current_directory, IMAGE_TO_ADD)
marker_image = pygame.image.load(marker_image_path)
marker_image = pygame.transform.scale(marker_image, (GRID_SIZE, GRID_SIZE))

# Button setup
toggle_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 10, 100, 40)
add_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 60, 100, 40)
grid_visible = True

# Store placed markers
placed_markers = []


def draw_grid():
    """Draws a grid overlay on the screen and displays x, y coordinates with origin at bottom-left."""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, WINDOW_HEIGHT))
            pygame.draw.line(screen, (200, 200, 200), (0, y), (WINDOW_WIDTH, y))
            coord_y = (WINDOW_HEIGHT - y) // GRID_SIZE - 1  # Inverted y-coordinate
            coord_x = x // GRID_SIZE
            coord_text = font.render(f"{coord_x},{coord_y}", True, TEXT_COLOR)
            screen.blit(coord_text, (x + 5, y + 5))


def draw_button(rect, text):
    """Draws a button with the given rect and text."""
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    button_text = font.render(text, True, TEXT_COLOR)
    screen.blit(button_text, (rect.x + 10, rect.y + 10))


def get_user_coordinates():
    """Opens a Tkinter dialog to get user input for grid coordinates."""
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    user_input = simpledialog.askstring("Input", "Enter coordinates (x,y):")
    root.destroy()
    if user_input:
        try:
            x, y = map(int, user_input.split(","))
            return x, y
        except ValueError:
            print("Invalid input. Please enter coordinates as x,y.")
    return None


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if toggle_button_rect.collidepoint(event.pos):
                grid_visible = not grid_visible
            elif add_button_rect.collidepoint(event.pos):
                coords = get_user_coordinates()
                if coords:
                    x, y = coords
                    if 0 <= x * GRID_SIZE < WINDOW_WIDTH and 0 <= (y + 1) * GRID_SIZE <= WINDOW_HEIGHT:
                        placed_markers.append((x, y))
                    else:
                        print("Coordinates out of bounds.")

    # Draw background
    screen.blit(background, (0, 0))

    # Draw grid if visible
    if grid_visible:
        draw_grid()

    # Draw buttons
    draw_button(toggle_button_rect, "Toggle Grid")
    draw_button(add_button_rect, "Add Image")

    # Draw placed markers
    for x, y in placed_markers:
        coord_x = x * GRID_SIZE
        coord_y = WINDOW_HEIGHT - (y + 1) * GRID_SIZE
        screen.blit(marker_image, (coord_x, coord_y))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
