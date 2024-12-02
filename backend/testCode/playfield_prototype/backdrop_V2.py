import pygame
import os
import tkinter as tk
from tkinter import simpledialog

# Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 50
BACKGROUND_IMAGE = "background.png"
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 150, 255)
TEXT_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Graph Visualization")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Load the background image
current_directory = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_directory, BACKGROUND_IMAGE)
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load marker images
marker_images = {}
for i in range(1, 4):  # Load marker1.png to marker2.png
    marker_path = os.path.join(current_directory, f"marker{i}.png")
    if os.path.exists(marker_path):
        marker_image = pygame.image.load(marker_path)
        marker_images[f"marker{i}"] = pygame.transform.scale(marker_image, (GRID_SIZE, GRID_SIZE))
    else:
        print(f"Warning: {marker_path} not found!")

# Buttons
toggle_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 10, 100, 40)
add_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 60, 100, 40)
edge_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 110, 100, 40)
grid_visible = True

# Graph Data Structures
graph = {
    "nodes": [],  # Store nodes as dictionaries with id, type, and coordinates
    "edges": []   # Store edges as dictionaries with start, end, and properties
}
node_counter = 0  # Unique ID counter for nodes
edge_mode = False  # Toggle edge creation mode
selected_nodes = []  # Nodes selected for edge creation


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



def get_user_input():
    """Opens a Tkinter dialog with two separate input fields for marker type and coordinates."""
    class CustomDialog(simpledialog.Dialog):
        def body(self, master):
            tk.Label(master, text="Marker Type (e.g., marker1):").grid(row=0, column=0, padx=5, pady=5)
            self.marker_type_entry = tk.Entry(master)
            self.marker_type_entry.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(master, text="Coordinates (x, y):").grid(row=1, column=0, padx=5, pady=5)
            self.coords_entry = tk.Entry(master)
            self.coords_entry.grid(row=1, column=1, padx=5, pady=5)

            return self.marker_type_entry  # Set focus on the first entry

        def apply(self):
            self.marker_type = self.marker_type_entry.get()
            coords = self.coords_entry.get()
            try:
                x, y = map(int, coords.split(","))
                self.result = (self.marker_type, (x, y))
            except ValueError:
                self.result = None  # Return None if input is invalid

    # Create the custom dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    dialog = CustomDialog(root, "Add Marker")
    root.destroy()

    return dialog.result if dialog.result else (None, None)

def get_edge_input():
    """Opens a Tkinter dialog with two separate input fields for marker type and coordinates."""
    class CustomDialog(simpledialog.Dialog):
        def body(self, master):
            tk.Label(master, text="Co-ordinates of Node 1:").grid(row=0, column=0, padx=5, pady=5)
            self.edge_start = tk.Entry(master)
            self.edge_start.grid(row=0, column=1, padx=5, pady=5)

            tk.Label(master, text="Co-ordinates of Node 2:").grid(row=1, column=0, padx=5, pady=5)
            self.edge_end = tk.Entry(master)
            self.edge_end.grid(row=1, column=1, padx=5, pady=5)

            return None

        def apply(self):
            coords1 = self.edge_start.get()
            coords2 = self.edge_end.get()
            try:
                x1, y1 = map(int, coords1.split(","))
                x2, y2 = map(int, coords2.split(","))

                self.result = ((x1, y1), (x2, y2))

            except ValueError:
                self.result = None  # Return None if input is invalid
            
    # Create the custom dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    dialog = CustomDialog(root, "Select Two Nodes to join")
    root.destroy()

    return dialog.result if dialog.result else (None, None)

def draw_nodes():
    """Draw all nodes with optional highlighting for selected nodes."""
    for node in graph["nodes"]:
        coord_x = node["coords"][0] * GRID_SIZE
        coord_y = WINDOW_HEIGHT - (node["coords"][1] + 1) * GRID_SIZE
        # Highlight if the node is selected
        if node in selected_nodes:
            pygame.draw.rect(screen, (255, 255, 0), (coord_x, coord_y, GRID_SIZE, GRID_SIZE))
        screen.blit(marker_images[node["type"]], (coord_x, coord_y))

def draw_edges(coord1, coord2):
    """Draw an edge between two given coordinates."""
    # Unpack the coordinates
    x1, y1 = coord1
    x2, y2 = coord2

    # Convert coordinates to the screen space (scaled to grid size)
    start_x = x1 * GRID_SIZE + GRID_SIZE // 2
    start_y = WINDOW_HEIGHT - (y1 + 1) * GRID_SIZE + GRID_SIZE // 2
    end_x = x2 * GRID_SIZE + GRID_SIZE // 2
    end_y = WINDOW_HEIGHT - (y2 + 1) * GRID_SIZE + GRID_SIZE // 2

    # Draw the line (edge) between the two coordinates
    pygame.draw.line(screen, (255, 0, 0), (start_x, start_y), (end_x, end_y),5 )

    pygame.draw.circle(screen, (0, 255, 0), (start_x, start_y), 5)  # Green circle at start
    pygame.draw.circle(screen, (0, 255, 0), (end_x, end_y), 5)      # Green circle at end


# Main loop
running = True
while running:
    coords2 = 0,0
    coords1 = 0,0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if toggle_button_rect.collidepoint(event.pos):
                grid_visible = not grid_visible
            elif add_button_rect.collidepoint(event.pos):
                marker_type, coords = get_user_input()
                if coords and marker_type in marker_images:
                    x, y = coords
                    if 0 <= x * GRID_SIZE < WINDOW_WIDTH and 0 <= (y + 1) * GRID_SIZE <= WINDOW_HEIGHT:
                        node = {"id": node_counter, "type": marker_type, "coords": (x, y)}
                        graph["nodes"].append(node)
                        node_counter += 1
                    else:
                        print("Coordinates out of bounds.")
                elif marker_type not in marker_images:
                    print(f"Invalid marker type: {marker_type}")
            elif edge_button_rect.collidepoint(event.pos):
                c1, c2 = get_edge_input()
                #coords1 = (x1, y1)
                #coords2 = (x2, y2)
                
                #print(f"x1 {x1}")
                #print(f"y1 {y1}")
                #print(f"x2 {x2}")
                #print(f"y2 {y2}")

    # Draw background
    screen.blit(background, (0, 0))

    # Draw grid if visible
    if grid_visible:
        draw_grid()

    # Draw buttons
    draw_button(toggle_button_rect, "Toggle Grid")
    draw_button(add_button_rect, "Add Marker")
    draw_button(edge_button_rect, "Edge Mode")

    # Draw edges and nodes
    draw_nodes()
    draw_edges(coords1, coords2)
    
    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()