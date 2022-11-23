import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.get_channel(409058658190753794).send("Jdeme hrát " + vyherni_hra + ", chce se někdo přidat?")
  # anaconda problem
  exit()

def StartBot(vyherni_h):
  global vyherni_hra
  vyherni_hra = vyherni_h
  client.run("MTA0NDU2ODA0ODc4NDM5NjM3OA.GAqm82.ggkQ8g38YsPCYj0eiNDud357C1KaIhr0Kq6oGc")

