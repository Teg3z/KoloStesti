"""
discord_bot.py

This module handles all the Discord bot interactions between the Wheel_of_luck and Discord Server. 

Main Functions:
- on_ready: An event handler for when the Discord bot is succesfully logged in.
- send_message: Sends a message via the Discord bot to a specified channel.
- get_reaction_users: Retrieves a list of users that put any reaction on the specific message.
- run_bot: The main starting point of the Discord bot.
- logout: Closing the currently opened Discord client.

Dependencies:
- Requires asyncio for establishing an event loop that can be accessed from the main wheel_of_luck
and by Discord events.
- Requires discord for interactions with the Discord servers.
- Requires db_handler to provide all database operations.
- Requires env_var_loader to load environment variables.
"""

import sys
import asyncio
import discord

from db_handler import DbHandler
from env_var_loader import get_env_var_value

class DiscordBot:
    def __init__(self) -> None:

        # Getting environment variables
        self.token = get_env_var_value("DISCORD_BOT_TOKEN")

        # Discord API needs the CHANNEL_ID in form of an integer, not string
        try:
            self.text_channel_id = int(get_env_var_value("TEST_CHANNEL_ID"))
        except (TypeError, ValueError):
            print("Invalid DISCORD_CHANNEL_ID. Must be an integer.")
            sys.exit(1)

        # Declaring Intents for the Discord Client
        self.intents = discord.Intents.default()
        self.intents.message_content = True

        # Initialize the Discord client
        self.client = discord.Client(intents=self.intents)

        # Setup database connection
        self.db = DbHandler()

        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    def run_bot(self) -> None:
        """
        The main starting point of the Discord bot.
        Creates a new event loop and starts a Discord client which takes control of the event loop,
        meaning listening to events from Discord servers.

        Returns:
            None
        """
        asyncio.run(self.client.start(self.token))

    async def logout(self) -> None:
        """
        Closing the currently opened Discord client, meaning the Discord bot logging off. 

        Returns:
            None
        """
        await self.client.close()

    async def on_ready(self) -> None:
        """
        An event handler for when the Discord bot is succesfully
        logged in and ready to receive commands.
        
        Only announces that the bot is ready in the console.

        Returns:
            None
        """
        print(f"We have logged in as {self.client.user}")

    async def on_message(self, message: discord.Message) -> None:
        """
        An event handler for when there is a message sent in the Discord
        channel where the bot is connected in.
        The bot ignores its own messages and reacts to specific commands starting
        with symbol "!" like "!games", "!mygames" etc.

        Returns:
            None
        """
        # Ensure the bot doesn't respond to itself
        if message.author == self.client.user:
            return
        # Check if the message starts with "!games"
        if message.content.startswith("!"):
            if message.content == "!games":
                # Ensure no extra spaces or newlines are present in each game name
                await message.channel.send(
                    "Games list: \n\n" +
                    f"{make_list_printable(self.db.get_list_of_games())}"
                )
            elif message.content.startswith("!games add "):
                # Extract the game name
                game = get_game_name_from_command(message, "!games add ")

                added = self.db.add_game_to_game_list(game)
                if added:
                    await message.channel.send(
                        f"'{game}' was succesfully added into the game list."
                    )
                else:
                    await message.channel.send(
                        f"'{game}' is already on the game list. (!games)"
                    )
            elif message.content.startswith("!games remove "):
                # Extract the game name
                game = get_game_name_from_command(message, "!games remove ")

                removed = self.db.remove_game_from_game_list(game)
                if removed:
                    await message.channel.send(
                        f"'{game}' was succesfully removed from the game list."
                    )
                else:
                    await message.channel.send(
                        f"'{game}' is not on the game list. (!games)"
                    )
            elif message.content == "!mygames":
                # Get the games list of the author of the message
                users_games = self.db.get_list_of_user_games(message.author.name)
                if len(users_games) == 0:
                    await message.channel.send(
                        "Your game list is empty, add games via: \"!mygames add League of Legends\""
                    )
                else:
                    await message.channel.send(
                        f"Your game list: \n\n{make_list_printable(users_games)}"
                    )
            elif message.content.startswith("!mygames add "):
                # Extract the game name
                game = get_game_name_from_command(message, "!mygames add ")

                if game in self.db.get_list_of_games():
                    self.db.add_game_to_user_game_list(message.author.name, game)
                    await message.channel.send(
                        f"'{game}' was sucesfully added into your game list."
                    )
                else:
                    await message.channel.send(
                        f"'{game}' wasn't found in the servers game list. (!games)"
                    )
            elif message.content.startswith("!mygames remove "):
                # Extract the game name
                game_to_remove = get_game_name_from_command(message, "!mygames remove ")

                if game_to_remove in self.db.get_list_of_user_games(message.author.name):
                    self.db.remove_game_from_user_game_list(message.author.name, game_to_remove)
                    await message.channel.send(
                        f"'{game_to_remove}' was succesfully removed from your game list."
                    )
                else:
                    await message.channel.send(
                        f"'{game_to_remove}' wasn't found in your game list. (!mygames)"
                    )

    async def send_message(
            self,
            message: discord.Message,
            channel_id = None
        ) -> int:
        """
        Sends a message via the Discord bot to a specified channel.

        Parameters:
            message (string): The message to be sent.
            discord_channel_id (int, optional): The channel where the message will be sent.
                Defaults to None.

        Returns:
            int: Discord ID of the sent message.
        """
        if channel_id is None:
            channel_id = self.text_channel_id

        message = await self.client.get_channel(channel_id).send(message)
        return message.id
    
    async def get_reaction_users(self, message_id: int, channel_id = None) -> list[str]:
        """
        Retrieves a list of users that put any reaction on the specific message in Discord chat.

        Parameters:
            message_id (int): The message's Discord ID.
            discord_channel_id (int, optional): The channel where the message is located.
                Defaults to DISCORD_CHANNEL_ID.

        Returns:
            List: A list of users that had at least one reaction on the message with message_id.
        """
        if channel_id is None:
            channel_id = self.text_channel_id

        channel = self.client.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        # Use a set to store unique user names
        users = set()

        for reaction in message.reactions:
            reaction_users = [user.name async for user in reaction.users()]
            users.update(reaction_users)

        return list(users)

def get_game_name_from_command(
        command: discord.Message,
        command_to_remove_from_message: str
    ) -> str:
    """
    Removes all of the string which doesn't represent a game name.

    Parameters:
        command (string): A message command posted by the user in Discord.
        command_to_remove_from_message (string):
            Part of the command that is to be removed in order to get the game name.

    Returns:
        string: Game name.
    """
    return command.content[len(command_to_remove_from_message):].strip()

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

async def main() -> None:
    """
    The main entry point of the script.

    Only used for testing this module.

    Returns:
        None 
    """
    # Create a new Discord bot
    bot = DiscordBot()

    # Start the Discord bot client
    await bot.run_bot()

    # Testing
    await bot.send_message("Just Testing")

    # On terminating the code
    await bot.logout()

if __name__ == '__main__':
    asyncio.run(main())
