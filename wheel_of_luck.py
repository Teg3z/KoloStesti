import random
import time
import PySimpleGUI
import discord_bot
from datetime import datetime
from game import Game
from db_handler import connect_to_db
from db_handler import get_list_of_users_games
import asyncio
import threading

# returns the whole LastSpin record in a string form
def get_last_spin_string(db):
    collection = db['LastSpin']
    entry = collection.find_one()
    return entry['last_category'] + " - " + entry['last_game'] + " [" + entry['last_game_date'] + "]" 
    
def insert_last_spin_into_database(db, game, category = None, players = None):
    # Create the time of the spin
    time = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    
    # Select the correct collection from the DB and create the new data values to enter
    if players is not None:
        collection = db['LastSpinReaction']
        new_values = { "$set": { 
        "last_game": game,
        "last_game_date": time,
        "players": players
         }
    }
    elif category is not None:
        collection = db['LastSpin']
        new_values = { "$set": { 
        "last_category" : category,
        "last_game": game,
        "last_game_date": time
         }
    }

    # Get the single entry that will be updated
    entry = collection.find_one()
    filter = {'_id': entry['_id']}
    
    collection.update_one(filter, new_values)

def insert_log_into_database(db, result):
    collection = db['LastSpin']
    entry = collection.find_one()
    collection = db["Logs" + entry['last_category']]

    post = {"game_date": entry['last_game_date'],
            "game": entry['last_game'],
            "result": result}

    collection.insert_one(post)

def remove_unwated_games(games_ui_texts, games, window, players):
    wanted_games_ui_texts = []
    wanted_games = []

    for index in range(0,len(games_ui_texts)):
        if players in games[index].players:
            window[games_ui_texts[index].key].Update(visible = True)
            wanted_games_ui_texts.append(games_ui_texts[index])
            wanted_games.append(games[index])
        else:
            window[games_ui_texts[index].key].Update(visible = False)

    window.refresh()  
    return wanted_games_ui_texts, wanted_games

def remove_unwated_games_reactions_based(games_ui_texts, games, window, common_games):
    wanted_games_ui_texts = []
    wanted_games = []

    for index in range(0,len(games_ui_texts)):
        if games[index].name in common_games:
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

def spin_wheel(games_ui_texts, games, main_window, result_ui):
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
    result_ui.update("\nUžijte si " + rolled_game_ui_text.Get())
    main_window.refresh()

    return rolled_game_ui_text

def start_discord_bot():
    bot_thread = threading.Thread(target=discord_bot.run_bot, daemon=True)
    bot_thread.start()
    return bot_thread

def send_message_to_discord(message):
    # Run the send_message coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(discord_bot.send_message(message), discord_bot.client.loop)
    message_id = future.result()
    return message_id

def get_reactions_users(message_id):
    # Run the send_message coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(discord_bot.get_reactions_users(message_id), discord_bot.client.loop)
    users = future.result()
    return users

def logout_discord_bot():
    asyncio.run_coroutine_threadsafe(discord_bot.logout(), discord_bot.client.loop)

async def main():
    db = connect_to_db()

    # Start the Discord bot
    bot_thread = start_discord_bot()

    # All the playable games
    apex = Game("Apex Legends", ["DK", "D", "K", "DKKA", "DKA"], 1)
    pubg = Game("PUBG: Battlegrounds", ["DK", "K", "D", "DKKA", "DKA",], 1)
    csgo = Game("Counter Strike: Global Offensive", ["DK", "D", "DKKA", "DKA",], 1)
    fortnite = Game("Fortnite", ["DK", "D"], 1)
    programming = Game("Programovani kola stesti", ["DK", "D", "DKKA", "DKA"], 1)
    lost_ark = Game("Lost Ark", ["DK", "D", "K", "DFK"], 1)
    #payday2 = Game("Payday 2", ["DFK", "DK", "FK", "F", "K"], 1)
    lolko = Game("League of Legends", ["DM", "D", "M", "DF", "DFKM"], 1)
    fall_guys = Game("Fall Guys", ["DFK", "DK", "DF", "FK", "D", "K", "F"], 1)
    overwatch = Game("Overwatch", ["DFK", "DK", "DF", "FK", "D", "K", "F", "DKKA", "DKA"], 1)
    gta = Game("Grant Treft Auto V", ["DFK", "F", "DK", "DF"], 1)
    keep_talking = Game("Keep Talking and Nobody Explodes", ["DK", "DF", "TEST"], 1)
    orcs = Game("Orcs Must Die", ["DK", "K"], 1)
    deceive = Game("Deceive", ["DFK", "DK", "DF"], 1)
    dead_by_daylight = Game("Dead by Daylight", ["DK", "DKKA", "DKA"], 1)
    dying_light = Game("Dying Light", ["DKKA", "DKA"], 1)

    games = [apex, pubg, csgo, fortnite, programming, lost_ark, lolko, fall_guys, overwatch, gta, keep_talking, orcs, deceive, dead_by_daylight, dying_light]

    # Colors
    bg_color = "Black"
    fg_color = "White"
    btn_color = "Green"
    btn_mouseover_color = "DarkGreen"
    btn_size = (7, 0)

    # Fonts
    font = ("Arial", 18)

    # Texts
    result_ui = PySimpleGUI.Text("", text_color=fg_color, background_color=bg_color, font=font)
    last_game_result = get_last_spin_string(db)
    last_game_result_ui = PySimpleGUI.Text(f"\nJak dopadla minulá hra? ({last_game_result})", text_color=fg_color, background_color=bg_color, font=font)
    winlose = PySimpleGUI.Text("", text_color=fg_color, background_color=bg_color, font=font)

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
    test_button = PySimpleGUI.Button("TEST", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
    announce_button = PySimpleGUI.Button("ANNOUNCE", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
    send_reaction_message_button  = PySimpleGUI.Button("SEND REACTION", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)
    play_by_reactions_button  = PySimpleGUI.Button("PLAY REACTION", button_color=btn_color, font=font, mouseover_colors=btn_mouseover_color, size=btn_size)


    # Layout creation
    layout = []

    # Adding game texts
    for _ui_game_text in games_ui_texts:
        layout.append([_ui_game_text])

    # Adding buttons
    layout.append([result_ui])
    layout.append([dk_button, dfk_button, d_button, dfkm_button, df_button, dkka_button, dka_button, test_button])
    layout.append([send_reaction_message_button, play_by_reactions_button])
    layout.append([announce_button])
    layout.append([last_game_result_ui])
    layout.append([win, lose])
    layout.append([winlose])

    # Applications main window setup
    main_window = PySimpleGUI.Window(title="Wheel of Luck", layout=layout, background_color=bg_color, use_default_focus=False)

    # Winning game
    rolled_game = games_ui_texts[0]

    # Each iteration represents a wheel spin
    while True:
        # Reads values from the applications main window
        event, values = main_window.read()

        # Pressing W/L buttons condition
        if event == "W":
            winlose.update("\n YOU ARE THE BEST" )
            insert_log_into_database(db, event)
            continue
        elif event == "L":
            winlose.update("\n YOU SUCK" )
            insert_log_into_database(db, event)
            continue
        elif event == "SEND REACTION":
            message_id = send_message_to_discord("Jde se točit kolem štěští! Kdo se zapojí?")
            continue
        elif event == "PLAY REACTION":
            players = get_reactions_users(message_id)

            # No reaction case
            if not players:
                send_message_to_discord("Nikdo nechce točit :(")
                continue

            # Get list of games that those players have in common
            is_first_player = True 
            for player in players:
                # Inicialize the list of common games by the first player
                if is_first_player:
                    common_games = get_list_of_users_games(db, player)
                    is_first_player = False
                    continue
                # Get current players list of games
                player_games = get_list_of_users_games(db, player)
                
                # Keep only the games that are still in the common_games list and also in the current players list 
                updated_games_list = []
                for game in common_games:
                    if game in player_games:
                        updated_games_list.append(game)
                common_games = updated_games_list
            
            # Wheel setup and spinning
            wanted_games_ui_texts, wanted_games = remove_unwated_games_reactions_based(games_ui_texts, games, main_window, common_games)
            rolled_game = spin_wheel(wanted_games_ui_texts, wanted_games, main_window, result_ui)
            insert_last_spin_into_database(db, rolled_game.Get(), players=players)
            continue
        elif event == "ANNOUNCE":
            # Call Discord Bot to announce the game that has been rolled
            send_message_to_discord("Jdeme hrát " + rolled_game.Get() + ", chce se někdo přidat?")
            continue
        # Wheel spin event
        elif event != PySimpleGUI.WIN_CLOSED:
            wanted_games_ui_texts, wanted_games = remove_unwated_games(games_ui_texts, games, main_window, event)
            rolled_game = spin_wheel(wanted_games_ui_texts, wanted_games, main_window, result_ui)
            insert_last_spin_into_database(db, rolled_game.Get(), category=event)
            continue
        # Window closing event
        # Properly shutting down the bot and its loop
        logout_discord_bot()
        # Wait for the logout operation to end, closing the discord bot thread
        bot_thread.join()
        break

if __name__ == "__main__":
    asyncio.run(main())
