# importy
import random
import time
import PySimpleGUI as grafika
import discord_bot
from datetime import datetime
from Hra import Hra
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

###
# pripoj se k DB
# databaze
uri = "REPLACED_DB_CONNECTION_STRING"
# # Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# create database
db = client['WheelOfLuck']

def ZjistiCoJsmeTociliNaposled():
    collection = db['LastSpin']
    entry = collection.find_one()
    return entry['last_game'] 
    

# zapis posledni toceni do tabulky v MongoDB
def ZapisDoMongoDBLastSpin(kategorie, posledni_hra):
    collection = db['LastSpin']

    entry = collection.find_one()

    filter = {'_id': entry['_id']}

    # When was last game spinned
    game_time = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    
    newvalues = { "$set": { 
        "last_category" : kategorie,
        "last_game": posledni_hra,
        "last_game_date": game_time
         } 
        }
    
    collection.update_one(filter, newvalues)

# zapis vysledek posledniho toceni do tabulky v MongoDB
def ZapisDoMongoDBLog(vysledek):
    collection = db['LastSpin']
    entry = collection.find_one()
    collection = db["Logs" + entry['last_category']]

    post = {"game_date": entry['last_game_date'],
            "game": entry['last_game'],
            "result": vysledek}

    collection.insert_one(post)

# odstran hry podle katerogie, ktera je tocena
def RemoveUnwantedGames(list_her_grafika, list_her, window, kdo_chce_hrat):
    wanted_games_grafika = []
    wanted_games = []

    for index in range(0,len(list_her_grafika)):
        if kdo_chce_hrat in list_her[index].list_chticu:
            window[list_her_grafika[index].key].Update(visible = True)
            wanted_games_grafika.append(list_her_grafika[index])
            wanted_games.append(list_her[index])
        else:
            window[list_her_grafika[index].key].Update(visible = False)

    window.refresh()  
    return wanted_games_grafika, wanted_games

# Zobraz vsechny hry
def MakeAllVisible(list_konkretni, window):
    for hra in list_konkretni:
        window[hra.Get()].Update(visible = True)

# Udelej vsechny hry bilou barvou
def Vybel(list_konkretni):
    for hra_bila in list_konkretni:
        hra_bila.update(text_color='White')

# Vyber hru (class Hra), ktera padne pri toceni
def VyberVyherniHru(list_konkretni):
    procenta = []
    for hra in list_konkretni:
        procenta.append(hra.procenta)
    return random.choices(list(list_konkretni),weights=procenta, k=1)

# graficke toceni kola
def Toceni(list_her_grafika, list_her):
    Vybel(list_her_grafika)
    vyherni_hra_nazev = VyberVyherniHru(list_her)[0].nazev
    interval = 0.01
    konecny_cas = random.uniform(0.3, 0.8)
    
    for hra in list_her_grafika:
        if (hra.Get() == vyherni_hra_nazev):
            vyherni_hra_grafika = hra
    hra_bila = list_her_grafika[0]
    koncime = False

    while not koncime:
        for hra_zelena in list_her_grafika:
            hra_zelena.update(text_color='Lime')
            if hra_bila.key != hra_zelena.key:
                hra_bila.update(text_color='White')
            hra_bila = hra_zelena
            window.refresh()
            time.sleep(interval)
            if interval > konecny_cas and hra_bila == vyherni_hra_grafika:
                koncime = True
                break

            interval+=0.02    

    # vybrani viteze
    output.update("\nUžijte si " + vyherni_hra_grafika.Get())
    window.refresh()

    return vyherni_hra_grafika

# list her, ktere pripadaji v uvahu
apex = Hra("Apex Legends", ["DK", "D", "K", "DKKA", "DKA"], 1)
pubg = Hra("PUBG: Battlegrounds", ["DK", "K", "D", "DKKA", "DKA"], 1)
csgo = Hra("Counter Strike: Global Offensive", ["DK", "D", "DKKA", "DKA"], 1)
fortnite = Hra("Fortnite", ["DK", "D"],1)
programovani = Hra("Programovani kola stesti", ["DK", "D", "DKKA", "DKA"], 1)
lost_ark = Hra("Lost Ark", ["DK", "D", "K", "DFK"], 1)
#payday2 = Hra("Payday 2", ["DFK", "DK", "FK", "F", "K"], 1)
lolko = Hra("League of Legends", ["DM", "D", "M", "DF", "DFKM"], 1)
fall_guys = Hra("Fall Guys", ["DFK", "DK", "DF", "FK", "D", "K", "F"], 1)
overwatch = Hra("Overwatch", ["DFK", "DK", "DF", "FK", "D", "K", "F", "DKKA", "DKA"], 1)
gta = Hra("Grant Treft Auto V", ["DFK", "F", "DK", "DF"], 1)
keep_talking = Hra("Keep Talking and Nobody Explodes", ["DK", "DF"], 1)
orcs = Hra("Orcs Must Die", ["DK", "K"], 1)
deceive = Hra("Deceive", ["DFK", "DK", "DF"], 1)
dead_by_daylight = Hra("Dead by Daylight", ["DK", "DKKA", "DKA"], 1)
dying_light = Hra("Dying Light", ["DK", "DKKA", "DKA"], 1)

list_her = [apex, pubg, csgo, fortnite, programovani, lost_ark, lolko, fall_guys, overwatch, gta, keep_talking, orcs, deceive, dead_by_daylight, dying_light]

# barvy
back = "Black"
front = "White"

# font
nas_font = ("Arial", 18)

# texty
output = grafika.Text("", text_color=front, background_color=back, font = nas_font)
minula_hra = grafika.Text("\nJak dopadla minulá hra?", text_color=front, background_color=back, font = nas_font)
winlose = grafika.Text("", text_color=front, background_color=back, font = nas_font)

posledniHraText = "Naposledy točeno: " + ZjistiCoJsmeTociliNaposled()
posledniHra = grafika.Text(posledniHraText, text_color=front, background_color=back, font = nas_font)

list_her_grafika = []

# vytvor list textu z listu her
for hra in list_her:
    list_her_grafika.append(grafika.Text(hra.nazev, text_color=front, font = nas_font, background_color=back, key=hra.nazev))

# buttony
dk_button = grafika.Button("DK", button_color = 'Green', font = nas_font , mouseover_colors='DarkGreen', size = (7,0))
df_button = grafika.Button("DF", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
dfk_button = grafika.Button("DFK", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
d_button = grafika.Button("D", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
dfkm_button = grafika.Button("DFKM", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
dkka_button = grafika.Button("DKKA", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
dka_button = grafika.Button("DKA", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
w = grafika.Button("W", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))
l = grafika.Button("L", button_color = 'Green', font = nas_font, mouseover_colors='DarkGreen', size = (7,0))


# vytvor layout z danych her
layout = []

for hra in list_her_grafika:
    layout.append([hra])

# pridej buttony
layout.append([output])
layout.append([dk_button, dfk_button, d_button, dfkm_button, df_button, dkka_button, dka_button])
layout.append([minula_hra])
layout.append([w,l])
layout.append([winlose])
layout.append([posledniHra])

# vlastnosti okna
window = grafika.Window(title="Gamerský kolo", layout=layout, background_color="Black", use_default_focus=False)

# vyherce
konecna_vyherni_hra = list_her_grafika[0]

koho_jsme_tocili = ""

# beh kola
while True:
    # precteni okna
    event, values = window.read()

    # zmacknuti W nebo L
    if event == "W" or event == "L":
        if event == "W":
            winlose.update("\n YOU ARE THE BEST" )
        else:
            winlose.update("\n YOU SUCK" )
        ZapisDoMongoDBLog(event)
    # toceni
    elif event != grafika.WIN_CLOSED:
        G, H = RemoveUnwantedGames(list_her_grafika, list_her , window, event)
        konecna_vyherni_hra = Toceni(G,H)
        koho_jsme_tocili = event
    # zavreni okna
    else:
        ZapisDoMongoDBLastSpin(koho_jsme_tocili, konecna_vyherni_hra.Get())
        discord_bot.StartBot(konecna_vyherni_hra.Get())
        break

