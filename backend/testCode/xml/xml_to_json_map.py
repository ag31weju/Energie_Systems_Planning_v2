"""
Module: XML Parser and Manager + Json creater
This module provides functionality for managing a mapping of elements from scenario XML file
to a JSON file. The mapping is stored as a dictionary where the keys are coordinate pairs (x, y) as strings, and the values are element types.

Features:
1. Parse elements from an XML file and initialize the element map.
2. Save the element map to a JSON file.
3. Load the element map from a JSON file.
4. Add or update elements in the map programmatically.

"""

import os
import json


# Function to load the element map from a JSON file
def load_element_map(file_path):
    """Loads the element map from a JSON file. Returns an empty dictionary if the file does not exist."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}


# Function to save the element map to a JSON file
def save_element_map(element_map, file_path):
    """Saves the element map to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(element_map, file, indent=4)
        print(f"Element map saved to {file_path}")


# Function to add or update an element in the map
def add_or_update_element(element_map, xpos, ypos, element_type):
    """Adds or updates an element in the map."""
    element_map[f"{xpos},{ypos}"] = element_type


# Example usage of loading an XML file and converting it to JSON
def initialize_from_xml(xml_file_path, json_file_path):
    """Parses an XML file and initializes the element map."""
    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    elements = root.find(".//playfield/elements")

    # Initialize element map
    element_map = {}

    # Populate the map with data from the XML
    for elem in elements:
        element_type = elem.get("type")
        xpos = int(elem.get("xpos"))
        ypos = int(elem.get("ypos"))
        element_map[f"{xpos},{ypos}"] = element_type

    # Save the map to a JSON file
    save_element_map(element_map, json_file_path)
    return element_map
