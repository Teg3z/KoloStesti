"""
env_var_loader.py

A helper module for loading environment variables from variables.env file.

Main Functions:
- get_env_var_value: An event handler for when the Discord bot is succesfully logged in.

Dependencies:
- Requires dotenv to load environment variables from .env file.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='variables.env')

def get_env_var_value(env_var_name):
    """
    Gets the value of the environment variable provided.
    If the environment variable isn't found, then the code exits with status code 1.

    Parameters:
        env_var_name (string): The name of the environment variable to be loaded. 

    Returns:
        None
    """
    env_var_value = os.getenv(env_var_name)
    if env_var_value is None:
        print(f"Environment variable {env_var_name} weren't loaded correctly. Exiting...")
        # Exit with a non-zero status code to indicate an error
        sys.exit(1)
    return env_var_value

def main():
    """
    The main entry point of the script.

    Only used for testing this module.

    Returns:
        None 
    """
    get_env_var_value("DISCORD_BOT_TOKEN")

if __name__ == '__main__':
    main()
