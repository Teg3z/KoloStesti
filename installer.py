# @author: R4tmax
# Takes the main Python script of the file
# Automatically lints it a provides a binary depending on
# the OS which has launched the script

# Import block
import PyInstaller.__main__
import os

# Specify the path to your main Python code file
current_directory = os.getcwd()
SCRIPT_PATH = current_directory + r"\wheel_of_luck.py"

# Runs the PyInstaller main library
# DOCS: https://pyinstaller.org/en/stable/
def build_executable(script_path):
    PyInstaller.__main__.run([
        '--onefile',
        script_path
    ])

# Specify the root of the script
if __name__ == "__main__":
    # Call the build_executable function with the script path
    build_executable(SCRIPT_PATH)
