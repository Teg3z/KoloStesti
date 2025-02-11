"""
utils.py

A module containing utility functions for the project.
"""

from pathlib import Path
import json

def make_list_printable(items_list: list[str]) -> str:
    """
    Makes the lists items stripped of any extra white characters.
    Every item will be on its separate line.

    Parameters:
        items_list (List): The list of items to to be made printable.

    Returns:
        List: A new list of items from items_list separated by a new line.
    """
    return "\n".join(item.strip() for item in items_list)

def get_config_path() -> Path:
    # Create 'Config' folder in the app directory
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)
    print("Config directory: ", config_dir)
    
    # Return the full path to the config file
    return config_dir / "config.json"

def load_config() -> dict:
    config_path = get_config_path()
    if config_path.exists():
        try:
            with config_path.open("r") as config_file:
                return json.load(config_file)
        except:
            print("Failed to load configuration")
    return {}

def save_config(config) -> None:
    config_path = get_config_path()
    try:
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)
            print(f"Configuration saved to {config_path}")
    except:
        print("Failed to save configuration")
