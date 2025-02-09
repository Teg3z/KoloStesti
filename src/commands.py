"""
commands.py

A module containing the Command class and its subclasses that represent different commands.

Dependencies:
- Requires the ABC class for abstaction.
- Requires discord to interact with the Discord API.
- Requires the DiscordBot class to interact with the Discord bot.
- Requires the make_list_printable to adjust lists for printing.
"""

from abc import ABC, abstractmethod
import discord

from db_handler import DbHandler
from utils import make_list_printable

class Command(ABC):
    """
    An abstract class that represents a command.
    """
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, message: discord.Message) -> None:
        """
        Executes the command.

        Parameters:
            message (discord.Message): The message containing the command and its parameters.
        """

    def get_params(self, message: discord.Message) -> str:
        """
        Extracts the parameters from the message content

        Parameters:
            message (discord.Message): The message containing the command and its parameters.

        Returns:
            str: The parameters of the message.
        """
        return message.content[len(self.name):].strip()

class ListGamesCommand(Command):
    """
    A class that represents the !games command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Print the list of games in the database.
        """
        games_list = make_list_printable(self.db.get_list_of_games())
        await message.channel.send(f"Games list: \n\n{games_list}")

class AddGameCommand(Command):
    """
    A class that represents the !addgame command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Add a game to the database.
        """
        # Extract the game name
        game = self.get_params(message)

        added = self.db.add_game_to_game_list(game)
        if added:
            await message.channel.send(
                f"'{game}' was succesfully added into the game list."
            )
        else:
            await message.channel.send(
                f"'{game}' is already on the game list. (!games)"
            )

class RemoveGameCommand(Command):
    """
    A class that represents the !removegame command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Remove a game from the database.
        """
        # Extract the game name
        game = self.get_params(message)

        removed = self.db.remove_game_from_game_list(game)
        if removed:
            await message.channel.send(
                f"'{game}' was succesfully removed from the game list."
            )
        else:
            await message.channel.send(
                f"'{game}' is not on the game list. (!games)"
            )

class MyGamesCommand(Command):
    """
    A class that represents the !mygames command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Print the list of games of the message author.
        """
        # Get the games list of the author of the message
        users_games = self.db.get_list_of_user_games(message.author.name)
        if len(users_games) == 0:
            await message.channel.send(
                "Your game list is empty."
            )
        else:
            await message.channel.send(
                f"Your game list: \n\n{make_list_printable(users_games)}"
            )

class AddUserGameCommand(Command):
    """
    A class that represents the !add command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Add a game to the user's game list.
        """
        # Extract the game name
        game = self.get_params(message)

        if game in self.db.get_list_of_games():
            self.db.add_game_to_user_game_list(message.author.name, game)
            await message.channel.send(
                f"'{game}' was sucesfully added into your game list."
            )
        else:
            await message.channel.send(
                f"'{game}' wasn't found in the servers game list. (!games)"
            )

class RemoveUserGameCommand(Command):
    """
    A class that represents the !remove command.
    """
    def __init__(self, name: str, description: str, db: DbHandler) -> None:
        super().__init__(name, description)
        self.db = db

    async def execute(self, message) -> None:
        """
        Remove a game from the user's game list.
        """
        # Extract the game name
        game_to_remove = self.get_params(message)

        if game_to_remove in self.db.get_list_of_user_games(message.author.name):
            self.db.remove_game_from_user_game_list(message.author.name, game_to_remove)
            await message.channel.send(
                f"'{game_to_remove}' was succesfully removed from your game list."
            )
        else:
            await message.channel.send(
                f"'{game_to_remove}' wasn't found in your game list. (!mygames)"
            )

class HelpCommand(Command):
    """
    A class that represents the !help command.
    """
    def __init__(self, name: str, description: str, commands: list[Command]) -> None:
        super().__init__(name, description)
        self.commands = commands

    async def execute(self, message) -> None:
        """
        Print the list of commands.
        """
        cmd_names_and_descriptions = [
            command.name + ": " + command.description for command in self.commands
        ]
        await message.channel.send(
            f"Commands: \n\n{make_list_printable(cmd_names_and_descriptions)}"
        )
