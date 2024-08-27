"""
discord_bot.py

This module handles all the Discord bot interactions between the Wheel_of_luck and Discord Server. 

Main Functions:
- on_ready: An event handler for when the Discord bot is succesfully logged in.
- send_message: Sends a message via the Discord bot to a specified channel.
- get_reactions_users: Retrieves a list of users that put any reaction on the specific message.
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
import db_handler
from env_var_loader import get_env_var_value

# Getting environment variables
DISCORD_BOT_TOKEN = get_env_var_value("DISCORD_BOT_TOKEN")
# Use CHANNEL_ID env var for the actuall usage of the bot.
# Use TEST_CHANNEL_ID env var for testing purposes.
CHANNEL_ID = get_env_var_value("TEST_CHANNEL_ID")

# Discord API needs the CHANNEL_ID in form of an integer, not string
try:
    DISCORD_CHANNEL_ID = int(CHANNEL_ID)
except (TypeError, ValueError):
    print(f"Invalid DISCORD_CHANNEL_ID: {CHANNEL_ID}. Must be an integer.")
    sys.exit(1)

# Declaring Intents for the Discord Client
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Setup database connection
db = db_handler.connect_to_db()
games = db_handler.get_list_of_games(db)

@client.event
async def on_ready():
    """
    An event handler for when the Discord bot is succesfully
    logged in and ready to receive commands.
    Only announces that the bot is ready in the console.

    Returns:
        None
    """
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """
    An event handler for when there is a message sent in the Discord
    channel where the bot is connected in.
    The bot ignores its own messages and reacts to specific commands starting
    with symbol "!" like "!games", "!mygames" etc.

    Returns:
        None
    """
    # Ensure the bot doesn't respond to itself
    if message.author == client.user:
        return
    # Check if the message starts with "!games"
    if message.content.startswith("!"):
        if message.content == "!games":
            # Ensure no extra spaces or newlines are present in each game name
            await message.channel.send(f"List her v kole štěstí: \n\n{make_list_printable(games)}")
        elif message.content == "!mygames":
            # Get the games list of the author of the message
            users_games = db_handler.get_list_of_users_games(db, message.author.name)
            await message.channel.send(f"Tvůj list her: \n\n{make_list_printable(users_games)}")
        elif message.content.startswith("!mygames add "):
            # Extract the game name
            game_to_add = message.content[len("!mygames add "):].strip()

            if game_to_add in games:
                db_handler.add_game_to_users_games_list(db, message.author.name, game_to_add)
                await message.channel.send(
                    f"Hra '{game_to_add}' byla úspěšně přidána do tvého seznamu her."
                )
            else:
                await message.channel.send(
                    f"Hra '{game_to_add}' nebyla nalezena na seznamu her. (!games)"
                )
        elif message.content.startswith("!mygames remove "):
            # Extract the game name
            game_to_remove = message.content[len("!mygames remove "):].strip()

            if game_to_remove in games:
                db_handler.remove_game_from_users_games_list(db,message.author.name,game_to_remove)
                await message.channel.send(
                    f"Hra '{game_to_remove}' byla úspěšně odebrána z tvého seznamu her."
                )
            else:
                await message.channel.send(
                    f"Hra '{game_to_remove}' nebyla nalezena na seznamu her. (!games)"
                )

    # You can add more conditions here for other commands if needed

def make_list_printable(items_list):
    """
    Makes the lists items stripped of any extra white characters.
    Every item will be on its separate line.

    Parameters:
        items_list (List): The list of items to to be made printable.

    Returns:
        List: A new list of items from items_list separated by a new line.
    """
    return "\n".join(item.strip() for item in items_list)

async def send_message(message, discord_channel_id = DISCORD_CHANNEL_ID):
    """
    Sends a message via the Discord bot to a specified channel.

    Parameters:
        message (string): The message to be sent.
        discord_channel_id (int, optional): The channel where the message will be sent.
            Defaults to DISCORD_CHANNEL_ID.

    Returns:
        int: Discord ID of the sent message.
    """
    message = await client.get_channel(discord_channel_id).send(message)
    return message.id

async def get_reactions_users(message_id, channel_id = DISCORD_CHANNEL_ID):
    """
    Retrieves a list of users that put any reaction on the specific message in Discord chat.

    Parameters:
        message_id (int): The message's Discord ID.
        discord_channel_id (int, optional): The channel where the message is located.
            Defaults to DISCORD_CHANNEL_ID.

    Returns:
        List: A list of users that had at least one reaction on the message with message_id.
    """
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    # Use a set to store unique user names
    users = set()

    for reaction in message.reactions:
        reaction_users = [user.name async for user in reaction.users()]
        users.update(reaction_users)

    return list(users)

def run_bot(discord_bot_token = DISCORD_BOT_TOKEN):
    """
    The main starting point of the Discord bot.
    Creates a new event loop and starts a Discord client which takes control of the event loop,
    meaning listening to events from Discord servers.

    Parameters:
        discord_bot_token (string, optional): The token of the Discord bot.
            Defaults to DISCORD_BOT_TOKEN, found in .env file.

    Returns:
        None
    """
    asyncio.run(client.start(discord_bot_token))

async def logout():
    """
    Closing the currently opened Discord client, meaning the Discord bot logging off. 

    Returns:
        None
    """
    await client.close()

async def main():
    """
    The main entry point of the script.

    Only used for testing this module.

    Returns:
        None 
    """
    # Start the Discord bot
    await client.start(DISCORD_BOT_TOKEN)

    # Testing
    await send_message("Just Testing")

    # On terminating the code
    await logout()

if __name__ == '__main__':
    asyncio.run(main())
