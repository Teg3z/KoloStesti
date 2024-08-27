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
db = db_handler.connect_to_db()
games = db_handler.get_list_of_games(db)

# Create an asyncio Event
bot_ready_event = asyncio.Event()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    bot_ready_event.set()

@client.event
async def on_message(message):
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
                await message.channel.send(f"Hra '{game_to_add}' byla úspěšně přidána do tvého seznamu her.")
            else:
                await message.channel.send(f"Hra '{game_to_add}' nebyla nalezena na seznamu her. (!games)")
        elif message.content.startswith("!mygames remove "):
            # Extract the game name
            game_to_remove = message.content[len("!mygames remove "):].strip()

            if game_to_remove in games:
                db_handler.remove_game_from_users_games_list(db, message.author.name, game_to_remove)
                await message.channel.send(f"Hra '{game_to_remove}' byla úspěšně odebrána z tvého seznamu her.")
            else:
                await message.channel.send(f"Hra '{game_to_remove}' nebyla nalezena na seznamu her. (!games)")

    # You can add more conditions here for other commands if needed

# Makes the lists items stripped of any extra white characters and every item will be on its separate line
def make_list_printable(list):
    return "\n".join(item.strip() for item in list)

async def send_message(message):
    message = await client.get_channel(DISCORD_CHANNEL_ID).send(message)
    return message.id

async def get_reactions_users(message_id, channel_id = DISCORD_CHANNEL_ID):
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    # Use a set to store unique user names
    users = set()

    for reaction in message.reactions:
        reaction_users = [user.name async for user in reaction.users()]
        users.update(reaction_users)

    return list(users)

def run_bot():
    asyncio.run(client.start(DISCORD_BOT_TOKEN))

async def logout():
    await client.close()

def main():
    # Start the Discord bot as a task
    run_bot()

    #users = await get_reactions_users()

    # On terminating the code
    # await logout()

if __name__ == '__main__':
    main()

