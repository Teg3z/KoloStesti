import asyncio
import discord
import sys
from env_var_loader import get_env_var_value
from db_handler import connect_to_db
from db_handler import get_list_of_games
from db_handler import get_list_of_users_games

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
db = connect_to_db()
games = get_list_of_games(db)

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
          users_games = get_list_of_users_games(db, message.author.name)
          await message.channel.send(f"Tvůj list her: \n\n{make_list_printable(users_games)}")

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


async def start_bot():
  # Runs the bot asynchronously in the background since client.start is a blocking function
  asyncio.create_task(client.start(DISCORD_BOT_TOKEN))
  # Wait for the bot to login and then can continue the code with bot ready to operate
  await bot_ready_event.wait()

async def logout():
  await client.close()

async def main():
    # Start the Discord bot as a task
    await start_bot()

    # users = await get_reactions_users()

    # On terminating the code
    await logout()


if __name__ == '__main__':
    asyncio.run(main())

