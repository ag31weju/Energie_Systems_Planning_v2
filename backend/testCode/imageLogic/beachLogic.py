from utils import get_neighbors

def get_beach_image(xpos, ypos, element_map):
    neighbors = get_neighbors(xpos, ypos, element_map)

    # Define rules for determining the image
    rules = [
        # Beach normal cases
        ({"top": "grass", "right": "beach"}, "beach_normal.png"),

        # Beach corner cases
        ({"top": "beach", "right": "beach"}, "beach_corner.png"),
        ({"left": "beach", "bottom": "beach"}, "beach_corner_inverted.png"),
        
        # Beach edge cases
        ({"top": "beach", "bottom": None}, "beach_edge_vertical.png"),
        ({"left": "beach", "right": None}, "beach_edge_horizontal.png"),

        #beach upside down cases
        
        
        # Mixed terrain cases
        ({"top": "river", "right": "beach"}, "beach_river_corner.png"),
        ({"left": "sea", "bottom": "beach"}, "beach_sea_corner_inverted.png"),
    ]

    # Check each rule
    for conditions, image in rules:
        if all(neighbors.get(pos) == terrain for pos, terrain in conditions.items()):
            return image

    # Default fallback image
    return "beach_isolated.png"
