#Here @AG implement parser for the XML file
import os
import xml.etree.ElementTree as ET

# check if the xml is present in the right directory
print("Current working directory:", os.getcwd())
file_path = 'scenario.xml'

current_directory = os.path.dirname(os.path.abspath(__file__))

xml_file_path = os.path.join(current_directory, 'xml', 'scenario.xml')

print(current_directory)

tree = ET.parse(xml_file_path)  # Parse the XML file
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

# iterate through the xml to set the matrix
for elem in elements:
    element_type = elem.get('type')  # Get the 'type' of the element
    xpos = int(elem.get('xpos'))  # Get the 'xpos' attribute
    ypos = int(elem.get('ypos'))  # Get the 'ypos' attribute
    
    # Place the element in the matrix at the correct position
    playfield_matrix[ypos][xpos] = element_type

# Export the playfield matrix to a text file with each line separated by a ;
output_file_path = os.path.join(current_directory, 'playfield_matrix.txt')
with open(output_file_path, 'w') as f:
    for row in playfield_matrix:
        f.write(','.join([cell if cell else 'empty' for cell in row]) + ';\n')


print(f"Playfield matrix exported to {output_file_path}")

