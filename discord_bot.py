import discord

BOT_KLIC_PATH = r"REPLACED_PATH\KoloStesti\bot_klic.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.get_channel(REPLACED_CHANNEL_ID).send("Jdeme hrát " + vyherni_hra + ", chce se někdo přidat?")
  # anaconda problem
  await client.close()

def StartBot(vyherni_h):
  global vyherni_hra
  vyherni_hra = vyherni_h
  bot_klic_file = open(BOT_KLIC_PATH, "rt")
  bot_klic = bot_klic_file.read()

  client.run(bot_klic)

