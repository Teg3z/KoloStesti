import discord
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='variables.env')

# Getting environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print(str(DISCORD_BOT_TOKEN))
CHANNEL_ID=os.getenv("CHANNEL_ID")
print(str(CHANNEL_ID))

# Check whether we loaded all environment variables, if not we cannot proceed with the code
if (DISCORD_BOT_TOKEN or CHANNEL_ID) is None:
    print("Environment variables weren't loaded correctly. Exiting...")
    sys.exit(1)  # Exit with a non-zero status code to indicate an error

try:
    DISCORD_CHANNEL_ID = int(CHANNEL_ID)
except (TypeError, ValueError):
    print(f"Invalid DISCORD_CHANNEL_ID: {CHANNEL_ID}. Must be an integer.")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.get_channel(DISCORD_CHANNEL_ID).send("Jdeme hrát " + game + ", chce se někdo přidat?")
  # Anaconda problem???
  await client.close()

def StartBot(rolled_game):
  global game
  game = rolled_game

  client.run(DISCORD_BOT_TOKEN)

def main():
  StartBot("Just Testing")

if __name__ == '__main__':
    main()

