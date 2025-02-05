"""
utils.py

A module containing utility functions for the project.
"""

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
