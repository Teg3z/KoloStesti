import discord
import sys
from env_var_loader import get_env_var_value

# Getting environment variables
DISCORD_BOT_TOKEN = get_env_var_value("DISCORD_BOT_TOKEN")
CHANNEL_ID = get_env_var_value("CHANNEL_ID")

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

