from graph_to_scenario.scenario import Scenario

"""
This does image and JSON processing of the Scenario uploaded by the user.
Image is cropped and Json file is parsed and printed out(just for testing)

"""


def parse_json(json_file):
    '''
    Get the json file from frontend and using create_scenario.py, parse the json file for optimizer
    '''
    scenario = Scenario(json_file)
    scenario.initialize()
    





'''
How to Navigate to a File in a Sibling Folder Using pathlib
    -Import Path from pathlib.
    -Use Path(__file__).parent to get the current script's directory.
    -Use .parent on the current directory to move up one level (equivalent to cd.. in terminal).
    -Combine the parent directory with the sibling folder name and file name using / (e.g., parent_dir / "folder_name" / "file_name.json").
    -Use .exists() to check if the file exists before opening or processing it.
    -Open and process the file if it exists; otherwise, handle the case where it does not.
'''