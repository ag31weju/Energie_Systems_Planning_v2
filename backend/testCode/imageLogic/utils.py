def get_neighbors(xpos, ypos, element_map):
    """
    Retrieves the neighboring elements of a given coordinate.

    Args:
        xpos (int): The x-coordinate of the element.
        ypos (int): The y-coordinate of the element.
        element_map (dict): A dictionary representing the entire map with keys as 'x,y' and values as element types.

    Returns:
        dict: A dictionary of neighboring elements with keys as 'top', 'bottom', 'left', 'right'.
              Values are the types of the neighboring elements or None if the neighbor does not exist.
    """
    neighbors = {
        "top": element_map.get(f"{xpos},{ypos-1}", None),
        "bottom": element_map.get(f"{xpos},{ypos+1}", None),
        "left": element_map.get(f"{xpos-1},{ypos}", None),
        "right": element_map.get(f"{xpos+1},{ypos}", None),
    }
    return neighbors
