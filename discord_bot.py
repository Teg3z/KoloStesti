import discord
import sys
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

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}")
  await client.get_channel(DISCORD_CHANNEL_ID).send("Jdeme hrát " + game + ", chce se někdo přidat?")
  # Anaconda problem???
  # await client.close()

@client.event
async def on_message(message):
    # Ensure the bot doesn't respond to itself
    if message.author == client.user:
        return

    # Check if the message starts with "!games"
    if message.content.startswith("!games"):
        await message.channel.send("You invoked the games command!")

    # You can add more conditions here for other commands if needed

def StartBot(rolled_game):
  global game
  game = rolled_game

  client.run(DISCORD_BOT_TOKEN)

def main():
  StartBot("Just Testing")

if __name__ == '__main__':
    main()

