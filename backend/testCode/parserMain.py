"""
Main file to run the parser and create json file
Xml file taken from xml folder and saved  in json file as a dictionary
"""

import os
from xml_to_json_map import initialize_from_xml

# Define file paths
current_directory = os.path.dirname(os.path.abspath(__file__))

# Path for the XML file in the 'xml' folder
xml_file_path = os.path.join(current_directory, "xml", "scenario.xml")

# Ensure the 'json' folder exists
json_folder_path = os.path.join(current_directory, "json")
os.makedirs(json_folder_path, exist_ok=True)

# Path for the JSON file in the 'json' folder
json_file_path = os.path.join(json_folder_path, "element_map.json")

# Initialize the element map from the XML file and save it to JSON
element_map = initialize_from_xml(xml_file_path, json_file_path)

# Print the initialized map
print("Initialized Element Map:", element_map)
