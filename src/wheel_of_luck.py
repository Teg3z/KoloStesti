"""
wheel_of_luck.py

The main module.

Manages the application's UI, starts the corresponding Discord bot and sends it commands.
Maintains the wheel spinning logic and sends results into a MongoDB database.

Main Functions:
- remove_unwated_games:
    Hides every game in the wheels UI that isn't mentioned in the `common_games` parameter.
- choose_winning_game:
    Randomly chooses one game out of a list of Game objects based on their desire percentage.
- spin_wheel:
    The whole wheel spinning logic is in this function.
- send_message_to_discord:
    Sends a new coroutine to the thread that the Discord bot is running on,
    telling the bot to send a message on Discord.
- main:
    The main entry point of the application.

Dependencies:
- Requires asyncio to manage the event loop, so that the application can wait for coroutines,
    like waiting for Discord bot to send a message.
- Requires threading for running the Discord bot on a separate thread.
- Requires PySimpleGUI for the application's simple UI.
- Requires discord_bot to send commands to the Discord bot.
- Requires db_handler for all the databe operations and establishment.
"""

import random
import asyncio
import threading
import PySimpleGUI
import discord_bot
import db_handler

def remove_unwated_games(game_ui_texts, games, window, common_games):
    """
    Hides every game in the wheels UI that isn't mentioned in the `common_games` parameter.

    Parameters:
        games_ui_texts (PySimpleGUI.Text): UI texts of all the game names.
        games (list[Game]): A list of all games represented by Game objects.
        window (PySimpleGUI.Window): The main UI window of the application.
        common_games (list[string]): A list of game names that the players have in common.

    Returns:
        list[PySimpleGUI.Text]:
            Contains all UI texts of games that will be visible during the spin.
        list[Game]:
            Contains all the Game objects with the game names that the players have in common.
    """
    wanted_game_ui_texts = []
    wanted_games = []

    for index, game_ui_text in enumerate(game_ui_texts):
        if game_ui_text.key in common_games:
            window[game_ui_text.key].Update(visible = True)
            wanted_game_ui_texts.append(game_ui_text)
            # The lists games and game_ui_texts are in the same order, so indexing works
            wanted_games.append(games[index])
        else:
            window[game_ui_text.key].Update(visible = False)

    window.refresh()
    return wanted_game_ui_texts, wanted_games

def make_all_games_texts_visible(games_ui_texts, window):
    """
    Makes vibisle all UI game name texts in the main window of the application.

    Parameters:
        games_ui_texts (PySimpleGUI.Text): UI texts of all the game names.
        window (PySimpleGUI.Window): The main UI window of the application.

    Returns:
        None
    """
    for _text in games_ui_texts:
        # Get() function here gets the actuall string text of the ui_text
        window[_text.Get()].Update(visible = True)

def whiten_game_ui_text(games_ui_texts):
    """
    Makes the text of all UI texts white

    Parameters:
        games_ui_texts (PySimpleGUI.Text): UI texts of all the game names.

    Returns:
        None
    """
    for _text in games_ui_texts:
        _text.update(text_color='White')

def choose_winning_game(games):
    """
    Randomly chooses one game out of a list of Game objects based on their
    desire percentage.
    
    Parameters:
        games (list[str]): A list of game names.

    Returns:
        game.Game: A randomly chosen Game object.
    """

    winning_games = random.choices(list(games), k=1)
    return winning_games[0]

async def spin_wheel(games_ui_texts, games, main_window, result_ui):
    """
    The whole wheel spinning logic is in this function.
    
    Mimicks a wheel spin by changing the colors of the UI game texts and progressively
    slowing down until a certain spin speed and rolled game is reached.

    Parameters:
        games_ui_texts (PySimpleGUI.Text): UI texts of all game names.
        games (list[Game]): A list of games represented by Game objects.
        window (PySimpleGUI.Window): The main UI window of the application.
        result_ui (PySimpleGUI.Text): The UI text object where the spin result will be shown.

    Returns:
        PySimpleGUI.Text: The changed `result_ui` object containing the name of the resulting game.
    """
    # Start with all games whitened.
    whiten_game_ui_text(games_ui_texts)
    # Choose the name of the winning game
    rolled_game = choose_winning_game(games)

    # Find the UI text corresponding to the `rolled_game`
    rolled_game_ui_text = games_ui_texts[0]
    for _text in games_ui_texts:
        if _text.Get() == rolled_game:
            rolled_game_ui_text = _text

    # Initial values setup before the wheel spinning
    interval = 0.01
    min_spinning_time = random.uniform(0.3, 0.8)
    prev_text = games_ui_texts[0]
    end = False

    while not end:
        # Each loop represents a wheel move
        for curr_text in games_ui_texts:

            # Update the color of the currently seleted game UI text
            curr_text.update(text_color='Lime')

            # Update the color of the previously selected game UI text
            # When there is only one game, then don't update it
            if prev_text.key != curr_text.key:
                prev_text.update(text_color='White')
            # Set the current text as previous to get ready for the next move
            prev_text = curr_text
            # Update the UI changes in the window
            main_window.refresh()

            # After minimal time has passed stop at the rolled game
            if interval > min_spinning_time and curr_text == rolled_game_ui_text:
                end = True
                break

            # Increase the interval of the next spin, mimicking a spinning wheel
            await asyncio.sleep(interval)
            interval+=0.02

    # Print out the spin result
    result_ui.update("\nUžijte si " + rolled_game_ui_text.Get())
    main_window.refresh()

    return rolled_game_ui_text

def start_discord_bot():
    """
    Starts a new Thread for the Discord bot to run on.
    
    Returns:
        threading.Thread: A newly stared thread on which the Discord bot is running.
    """
    bot_thread = threading.Thread(target=discord_bot.run_bot, daemon=True)
    bot_thread.start()
    return bot_thread

def send_message_to_discord(message):
    """
    Sends a new coroutine to the thread that the Discord bot is running on,
    telling the bot to send a message on Discord.

    Parameters:
        message (string): A message to be sent via the Discord bot.

    Returns:
        int: The Discord ID of the sent message.
    """
    # Run the send_message coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(
        discord_bot.send_message(message),
        discord_bot.client.loop
    )
    message_id = future.result()
    return message_id

def get_reactions_users(message_id):
    """
    Sends a new coroutine to the thread that the Discord bot is running on,
    telling the bot to return a list of all Discord user names that put a reaction
    on the message with `message_id`.

    Parameters:
        message_id (int): A message to be sent via the Discord bot.

    Returns:
        list: A list of all user names that have reacted to the message.
    """
    # Run the send_message coroutine in the bot's event loop
    future = asyncio.run_coroutine_threadsafe(
        discord_bot.get_reaction_users(message_id),
        discord_bot.client.loop
    )
    users = future.result()
    return users

def logout_discord_bot():
    """
    Sends a new coroutine to the thread that the Discord bot is running on,
    telling the bot to log out, resulting in the closing of the event loop
    in the Discord bot thread.

    Returns:
        None
    """
    asyncio.run_coroutine_threadsafe(discord_bot.logout(), discord_bot.client.loop)

def change_last_spin_insertion_visibility(window, db, visible):
    """
    Handles visibility of the corresponding UI elements taking care of last spin
    insertion into the DB. 

    Parameters:
        window (PySimpleGUI.Window):
            The main UI window of the application.
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        visible (bool):
            Indicates whether the UI elements should be hidden/shown .

    Returns:
        None
    """
    window["W"].Update(visible=visible)
    window["L"].Update(visible=visible)
    window["LAST_GAME"].Update(visible=visible)
    if visible:
        window["LAST_GAME"].Update(value=db_handler.get_last_spin_string(db))

    window.refresh()

async def main():
    """
    The main entry point of the application.

    Establishes connection to MongoDB database and Discord bot.
    Sets all the UI elements and lays them out.
    Provides all the functionality that the UI elements should posses. 

    Returns:
        None 
    """
    # Establish database connection
    db = db_handler.connect_to_db()

    # Start the Discord bot
    bot_thread = start_discord_bot()

    # All the playable games
    games = db_handler.get_list_of_games(db)

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
    last_game_result = db_handler.get_last_spin_string(db)
    is_last_spin_inserted, _ = db_handler.is_last_spin_inserted(db)
    last_game_result_ui = PySimpleGUI.Text(
        f"\nLast game result? \n({last_game_result})",
        text_color=fg_color,
        background_color=bg_color,
        font=font,
        key="LAST_GAME",
        visible= not is_last_spin_inserted
    )

    win_lose_msg = PySimpleGUI.Text("", text_color=fg_color, background_color=bg_color, font=font)

    games_ui_texts = []

    for _game in games:
        games_ui_texts.append(PySimpleGUI.Text(
            _game,
            text_color=fg_color,
            font=font,
            background_color=bg_color,
            key=_game
        ))

    # Buttons
    win = PySimpleGUI.Button(
        "W",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size,
        visible=not is_last_spin_inserted
    )
    lose = PySimpleGUI.Button(
        "L",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size,
        visible=not is_last_spin_inserted
    )
    announce_button = PySimpleGUI.Button(
        "ANNOUNCE",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )
    send_reaction_message_button = PySimpleGUI.Button(
        "SEND REACTION",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )
    play_by_reactions_button = PySimpleGUI.Button(
        "PLAY REACTION",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )

    # Layout creation
    layout = []

    # Adding game texts
    for _ui_game_text in games_ui_texts:
        layout.append([_ui_game_text])

    # Adding buttons
    layout.append([result_ui])
    layout.append([send_reaction_message_button, play_by_reactions_button])
    layout.append([announce_button])
    layout.append([last_game_result_ui])
    layout.append([win, lose])
    layout.append([win_lose_msg])

    # Applications main window setup
    main_window = PySimpleGUI.Window(
        title="Wheel of Luck",
        layout=layout,
        background_color=bg_color,
        use_default_focus=False
    )

    # Initiate variables
    rolled_game = None
    message_id = None

    # Each iteration represents a wheel spin
    while True:
        # Reads values from the applications main window
        event, _ = main_window.read()

        # Pressing W/L buttons condition
        if event == "W":
            win_lose_msg.update("\nYOU ARE THE BEST")
            db_handler.insert_log_into_database(db, event)
            change_last_spin_insertion_visibility(main_window, db, False)
            continue
        if event == "L":
            win_lose_msg.update("\nYOU SUCK")
            db_handler.insert_log_into_database(db, event)
            change_last_spin_insertion_visibility(main_window, db, False)
            continue
        if event == "SEND REACTION":
            rolled_game = None
            message_id = send_message_to_discord("Let's spin the wheel of luck! Who's in?")
            continue
        if event == "PLAY REACTION":
            # Check that there is a message already sent in the DC chat
            if message_id is None:
                print("You have to send a reaction message first.")
                continue
            players = get_reactions_users(message_id)

            # No reaction case
            if not players:
                send_message_to_discord("Nobody wants to participate :(")
                continue

            # Get list of games that those players have in common
            is_first_player = True
            for player in players:
                # Inicialize the list of common games by the first player
                if is_first_player:
                    common_games = db_handler.get_list_of_user_games(db, player)
                    is_first_player = False
                    continue
                # Get current players list of games
                player_games = db_handler.get_list_of_user_games(db, player)
                # Keep only the games that are still in the common_games list
                # and also in the current players list
                updated_games_list = []
                for game in common_games:
                    if game in player_games:
                        updated_games_list.append(game)
                common_games = updated_games_list

            # Wheel setup and spinning
            wanted_game_ui_texts, wanted_games = remove_unwated_games(
                games_ui_texts,
                games,
                main_window,
                common_games
            )
            rolled_game = await spin_wheel(
                wanted_game_ui_texts,
                wanted_games,
                main_window,
                result_ui
            )
            db_handler.update_last_spin(db, rolled_game.Get(), players=players)
            # Show insertion
            change_last_spin_insertion_visibility(main_window, db, True)
            continue
        if  event == "ANNOUNCE":
            if rolled_game is not None:
                # Call Discord Bot to announce the game that has been rolled
                send_message_to_discord(
                    "Going to play " + rolled_game.Get() + ", anyone wanna join in?"
                )
            continue
        # Window closing event
        # Properly shutting down the bot and its loop
        logout_discord_bot()
        # Wait for the logout operation to end, closing the discord bot thread
        bot_thread.join()
        break

if __name__ == "__main__":
    # Create an event loop for the main function
    asyncio.run(main())
