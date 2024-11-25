#Here @AG implement parserfor the XML file

import xml.etree.ElementTree as ET

# check if the xml is present in the right directory
import os
file_path = r"C:\Users\49151\OneDrive\Desktop\energy_system_planning-1\backend\testCode\xml\scenario1.xml"
try:
    with open(file_path, 'r') as file:
        # check if the file is found and print the contents
        # content = file.read()
        # print(content)
        print("file found")
except FileNotFoundError:
    print(f"File not found: {file_path}")


file_path = r"C:\Users\49151\OneDrive\Desktop\energy_system_planning-1\backend\testCode\xml\scenario1.xml"

tree = ET.parse(file_path)  # Parse the XML file
root = tree.getroot()  # Get the root element of the XML

# dynamic selecting matrix size 
max_x = 0
max_y = 0

# Extract elements from the XML
elements = root.find(".//playfield/elements")  # Navigate to the elements section

# First pass: Determine the max_x and max_y values
for elem in elements:
    xpos = int(elem.get('xpos'))
    ypos = int(elem.get('ypos'))
    
    # Update max_x and max_y
    if xpos > max_x:
        max_x = xpos
    if ypos > max_y:
        max_y = ypos

# The matrix will have (max_y + 1) rows and (max_x + 1) columns
playfield_matrix = [['' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

#iterate through the xml to set the matrix
for elem in elements:
    element_type = elem.get('type')  # Get the 'type' of the element
    xpos = int(elem.get('xpos'))  # Get the 'xpos' attribute
    ypos = int(elem.get('ypos'))  # Get the 'ypos' attribute
    
    # Place the element in the matrix at the correct position
    playfield_matrix[ypos][xpos] = element_type

# Print the playfield matrix
for row in playfield_matrix:
    print('    '.join([cell if cell else 'empty' for cell in row]))  