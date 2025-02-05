"""
command_factory.py

A module containing the CommandFactory class that creates command objects
based on the message content.

Dependencies:
- Requires the commands module to get the command classes.
"""

import commands

class CommandFactory:
    """
    A class that returns command objects based on the message content.

    Main Functions:
    - get_command: Returns the appropriate command class based on the message content.

    Attributes:
    - commands (list): A list of all command classes.
    """
    def __init__(self) -> None:
        self.commands: list[commands.Command] = [
            commands.ListGamesCommand("!games "),
            commands.AddGameCommand("!addgame "),
            commands.RemoveGameCommand("!removegame "),
            commands.MyGamesCommand("!mygames "),
            commands.AddUserGameCommand("!add "),
            commands.RemoveUserGameCommand("!remove ")
        ]

    def get_command(self, message_content: str) -> commands.Command | None:
        """
        Returns the appropriate command class based on the message content.

        Parameters:
            message_content (str): The content of the message.

        Returns:
            Command: The command class that matches the message
        """
        possible_commands: list[commands.Command] = []

        # List all possible commands
        for command in self.commands:
            if message_content.startswith(command.name):
                possible_commands.append(command)

        # Return the command with the longest match
        max_len = 0
        matched_command = None

        for command in possible_commands:
            if len(command.name) > max_len:
                max_len = len(command.name)
                matched_command = command

        return matched_command
