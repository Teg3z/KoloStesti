import random
import time
import PySimpleGUI
import discord_bot
from datetime import datetime
from game import Game
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_var_loader import get_env_var_value

# Connect to the MongoDB server
DB_CONNECTION_STRING = get_env_var_value("DB_CONNECTION_STRING")
# Create a new client and connect to the server
client = MongoClient(DB_CONNECTION_STRING, server_api=ServerApi('1'))
# Create database
db = client['WheelOfLuck']

def get_last_game_played():
    collection = db['LastSpin']
    entry = collection.find_one()
    return entry['last_game'] 
    
def insert_last_spin_into_database(category, game):
    collection = db['LastSpin']

    entry = collection.find_one()

    filter = {'_id': entry['_id']}

    # When was last game spinned
    time = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    
    new_values = { "$set": { 
        "last_category" : category,
        "last_game": game,
        "last_game_date": time
         }
    }
    
    collection.update_one(filter, new_values)

def insert_log_into_database(result):
    collection = db['LastSpin']
    entry = collection.find_one()
    collection = db["Logs" + entry['last_category']]

    post = {"game_date": entry['last_game_date'],
            "game": entry['last_game'],
            "result": result}

    collection.insert_one(post)

def remove_unwated_games(games_ui_texts, games, window, kdo_chce_hrat):
    wanted_games_ui_texts = []
    wanted_games = []

    for index in range(0,len(games_ui_texts)):
        if kdo_chce_hrat in games[index].players:
            window[games_ui_texts[index].key].Update(visible = True)
            wanted_games_ui_texts.append(games_ui_texts[index])
            wanted_games.append(games[index])
        else:
            window[games_ui_texts[index].key].Update(visible = False)

    window.refresh()  
    return wanted_games_ui_texts, wanted_games

# Makes vibisle all games texts in the main window
def make_all_games_texts_visible(games_ui_texts, window):
    for _text in games_ui_texts:
        window[_text.Get()].Update(visible = True)

# Makes all texts of the games white
def whiten_game_ui_text(games_ui_texts):
    for _text in games_ui_texts:
        _text.update(text_color='White')

def choose_winning_game(games):
    percentages = []
    for _game in games:
        percentages.append(_game.percentage)
    return random.choices(list(games),weights=percentages, k=1)

def spin_wheel(games_ui_texts, games):
    whiten_game_ui_text(games_ui_texts)
    rolled_game = choose_winning_game(games)[0].name
    interval = 0.01
    min_spinning_time = random.uniform(0.3, 0.8)
    
    for _text in games_ui_texts:
        if (_text.Get() == rolled_game):
            rolled_game_ui_text = _text
    prev_text = games_ui_texts[0]
    end = False

    while not end:
        for curr_text in games_ui_texts:

            # Update the colors of the texts
            curr_text.update(text_color='Lime')
            # When there is only one game in the wheel
            if prev_text.key != curr_text.key:
                prev_text.update(text_color='White')
            prev_text = curr_text
            main_window.refresh()

            # After minimal time has passed stop at the rolled game 
            if interval > min_spinning_time and curr_text == rolled_game_ui_text:
                end = True
                break

            # Increase the interval of the next spin
            time.sleep(interval)
            interval+=0.02    

    # Print the spin result
    result.update("\nUžijte si " + rolled_game_ui_text.Get())
    main_window.refresh()

    return rolled_game_ui_text

# list her, ktere pripadaji v uvahu
apex = Game("Apex Legends", ["DK", "D", "K", "DKKA", "DKA"], 1)
pubg = Game("PUBG: Battlegrounds", ["DK", "K", "D", "DKKA", "DKA"], 1)
csgo = Game("Counter Strike: Global Offensive", ["DK", "D", "DKKA", "DKA"], 1)
fortnite = Game("Fortnite", ["DK", "D"], 1)
programming = Game("Programovani kola stesti", ["DK", "D", "DKKA", "DKA"], 1)
lost_ark = Game("Lost Ark", ["DK", "D", "K", "DFK"], 1)
#payday2 = Hra("Payday 2", ["DFK", "DK", "FK", "F", "K"], 1)
lolko = Game("League of Legends", ["DM", "D", "M", "DF", "DFKM"], 1)
fall_guys = Game("Fall Guys", ["DFK", "DK", "DF", "FK", "D", "K", "F"], 1)
overwatch = Game("Overwatch", ["DFK", "DK", "DF", "FK", "D", "K", "F", "DKKA", "DKA"], 1)
gta = Game("Grant Treft Auto V", ["DFK", "F", "DK", "DF"], 1)
keep_talking = Game("Keep Talking and Nobody Explodes", ["DK", "DF"], 1)
orcs = Game("Orcs Must Die", ["DK", "K"], 1)
deceive = Game("Deceive", ["DFK", "DK", "DF"], 1)
dead_by_daylight = Game("Dead by Daylight", ["DK", "DKKA", "DKA"], 1)
dying_light = Game("Dying Light", ["DKKA", "DKA"], 1)

games = [apex, pubg, csgo, fortnite, programming, lost_ark, lolko, fall_guys, overwatch, gta, keep_talking, orcs, deceive, dead_by_daylight, dying_light]

# colors
bg_color = "Black"
fg_color = "White"
btn_color = "Green"
btn_mouseover_color = "DarkGreen"
btn_size = (7, 0)

# font
font = ("Arial", 18)

# texts
result = PySimpleGUI.Text("", text_color=fg_color, background_color=bg_color, font=font)
last_game_result = PySimpleGUI.Text("\nJak dopadla minulá hra?", text_color=fg_color, background_color=bg_color, font=font)
winlose = PySimpleGUI.Text("", text_color=fg_color, background_color=bg_color, font=font)

last_game_text = "Naposledy točeno: " + get_last_game_played()
last_game_ui_text = PySimpleGUI.Text(last_game_text, text_color=fg_color, background_color=bg_color, font = font)

games_ui_texts = []

for _game in games:
    games_ui_texts.append(PySimpleGUI.Text(_game.name, text_color=fg_color, font=font, background_color=bg_color, key=_game.name))

# Buttons
dk_button = PySimpleGUI.Button("DK", button_color=btn_color, font=font , mouseover_colors=btn_mouseover_color, size=btn_size)
dfk_button = PySimpleGUI.Button("DFK", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
d_button = PySimpleGUI.Button("D", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
dfkm_button = PySimpleGUI.Button("DFKM", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
df_button = PySimpleGUI.Button("DF", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
dkka_button = PySimpleGUI.Button("DKKA", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
dka_button = PySimpleGUI.Button("DKA", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
win = PySimpleGUI.Button("W", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
lose = PySimpleGUI.Button("L", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)


# Layout creation
layout = []

# Adding game texts
for _ui_game_text in games_ui_texts:
    layout.append([_ui_game_text])

# Adding buttons
layout.append([result])
layout.append([dk_button, dfk_button, d_button, dfkm_button, df_button, dkka_button, dka_button])
layout.append([last_game_result])
layout.append([win, lose])
layout.append([winlose])
layout.append([last_game_ui_text])

# Applications main window setup
main_window = PySimpleGUI.Window(title="Wheel of Luck", layout=layout, background_color=bg_color, use_default_focus=False)

# Winning game
rolled_game = games_ui_texts[0]

button = ""

# Each iteration represents a wheel spin
while True:
    # Reads values from the applications main window
    event, values = main_window.read()

    # Pressing W/L buttons condition
    if event == "W":
        winlose.update("\n YOU ARE THE BEST" )
        insert_log_into_database(event)
        continue
    if event == "L":
        winlose.update("\n YOU SUCK" )
        insert_log_into_database(event)
        continue
    
    # Wheel spin event
    if event != PySimpleGUI.WIN_CLOSED:
        wanted_games_ui_texts, wanted_games = remove_unwated_games(games_ui_texts, games, main_window, event)
        rolled_game = spin_wheel(wanted_games_ui_texts, wanted_games)
        button = event
        continue

    # Window closing event
    insert_last_spin_into_database(button, rolled_game.Get())
    # Call Discord Bot to announce the game that has been rolled
    discord_bot.StartBot(rolled_game.Get())
    break
