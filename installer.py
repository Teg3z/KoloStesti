"""
installer.py

Takes the main Python script of the file, automatically lints it and provides
a binary depending on the OS which has launched the script.

Main Functions:
- build_executable: Runs the PyInstaller main library.

Dependencies:
- Requires pyinstaller that makes the actual conversion of the .py script to an executable.
"""

import os
import PyInstaller.__main__

# Specify the path to your main Python code file
current_directory = os.getcwd()
SCRIPT_PATH = current_directory + r"\wheel_of_luck.py"

def build_executable(script_path):
    """
    Runs the PyInstaller main library. DOCS: https://pyinstaller.org/en/stable/
    
    Parameters:
        script_path (string): A path to the main script of the application (wheel_of_luck.py).

    Returns:
        None
    """
    PyInstaller.__main__.run([
        '--onefile',
        script_path
    ])

# Specify the root of the script
if __name__ == "__main__":
    # Call the build_executable function with the script path
    build_executable(SCRIPT_PATH)
