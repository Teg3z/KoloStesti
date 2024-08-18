import discord
import os

curr_directory = os.getcwd()
DISCORD_BOT_KEY = curr_directory + r"\bot_key.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.get_channel(409058658190753794).send("Jdeme hrát " + game + ", chce se někdo přidat?")
  # anaconda problem
  await client.close()

def StartBot(rolled_game):
  global game
  game = rolled_game
  file = open(DISCORD_BOT_KEY, "rt")
  bot_key = file.read()

  client.run(bot_key)

