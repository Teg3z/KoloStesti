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
- Requires PySimpleGUI for the application's simple UI.
- Requires discord_bot to send commands to the Discord bot.
- Requires db_handler for all the databe operations and establishment.
"""

import random
import asyncio
import PySimpleGUI as sg
from pathlib import Path
import json

from discord_bot import DiscordBot
from db_handler import DbHandler

def remove_unwated_games(
        game_ui_texts: list[sg.Text],
        games: list[str],
        window: sg.Window,
        common_games: list[str]
    ) -> tuple[list[sg.Text], list[str]]:
    """
    Hides every game in the wheels UI that isn't mentioned in the `common_games` parameter.

    Parameters:
        games_ui_texts (sg.Text): UI texts of all the game names.
        games (list[Game]): A list of all games represented by Game objects.
        window (sg.Window): The main UI window of the application.
        common_games (list[string]): A list of game names that the players have in common.

    Returns:
        list[sg.Text]:
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

def make_all_games_texts_visible(
        games_ui_texts: list[sg.Text],
        window: sg.Window
        ) -> None:
    """
    Makes vibisle all UI game name texts in the main window of the application.

    Parameters:
        games_ui_texts (sg.Text): UI texts of all the game names.
        window (sg.Window): The main UI window of the application.

    Returns:
        None
    """
    for _text in games_ui_texts:
        # Get() function here gets the actuall string text of the ui_text
        window[_text.Get()].Update(visible = True)

def whiten_game_ui_text(games_ui_texts: list[sg.Text]) -> None:
    """
    Makes the text of all UI texts white

    Parameters:
        games_ui_texts (sg.Text): UI texts of all the game names.

    Returns:
        None
    """
    for _text in games_ui_texts:
        _text.update(text_color='White')

def choose_winning_game(games: list[str]) -> str:
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

async def spin_wheel(
        games_ui_texts: list[sg.Text],
        games: list[str],
        main_window: sg.Window,
        result_ui: sg.Text
        ) -> sg.Text:
    """
    The whole wheel spinning logic is in this function.
    
    Mimicks a wheel spin by changing the colors of the UI game texts and progressively
    slowing down until a certain spin speed and rolled game is reached.

    Parameters:
        games_ui_texts (sg.Text): UI texts of all game names.
        games (list[Game]): A list of games represented by Game objects.
        window (sg.Window): The main UI window of the application.
        result_ui (sg.Text): The UI text object where the spin result will be shown.

    Returns:
        sg.Text: The changed `result_ui` object containing the name of the resulting game.
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

def change_last_spin_insertion_visibility(window: sg.Window, db: DbHandler, visible: bool):
    """
    Handles visibility of the corresponding UI elements taking care of last spin
    insertion into the DB. 

    Parameters:
        window (sg.Window):
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
        window["LAST_GAME"].Update(value=db.get_last_spin_string())

    window.refresh()

# Settings Window Function
async def open_settings_window(font: str, bg_color: str, fg_color: str):
    # Load existing config
    config = load_config()

    # Default values for textboxes (use existing config values if available)
    dc_token = config.get("DISCORD_BOT_TOKEN", "")
    channel_id = config.get("CHANNEL_ID", "")
    db_connection = config.get("DB_CONNECTION_STRING", "")

    text_size = (15, 1)
    settings_layout = [
        [sg.Text(
            "Discord bot token:",
            size=text_size,
            font=font,
            background_color=bg_color,
            text_color=fg_color
            ), sg.InputText(default_text=dc_token, key='dc_token')],
        [sg.Text(
            "Channel ID:",
            size=text_size,
            font=font,
            background_color=bg_color,
            text_color=fg_color
            ), sg.InputText(default_text=channel_id ,key='channel_id')],
        [sg.Text(
            "MongoDB:",
            size=text_size,
            font=font,
            background_color=bg_color,
            text_color=fg_color
            ), sg.InputText(default_text=db_connection ,key='db_connection')],
        [sg.Button("Save", button_color="Green"), sg.Button("Cancel", button_color="Red")]
    ]
    settings_window = sg.Window(
        "Settings",
        layout=settings_layout,
        modal=True,
        background_color=bg_color
    )
    while True:
        event, values = settings_window.read(timeout=100)
        if event == "Save":
            config = {
                "DISCORD_BOT_TOKEN": values['dc_token'],
                "CHANNEL_ID": values['channel_id'],
                "DB_CONNECTION_STRING": values['db_connection']
            }
            print("Settings to be saved:", config)
            save_config(config)
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":
            break
        # Yield control back to the event loop
        await asyncio.sleep(0.1)
    settings_window.close()

def load_config():
    """Load configuration from the config file."""
    config_path = get_config_path()
    if config_path.exists():
        try:
            with config_path.open("r") as config_file:
                return json.load(config_file)
        except:
            print("Failed to load configuration")
    return {}

def save_config(config):
    config_path = get_config_path()
    try:
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)
            print(f"Configuration saved to {config_path}")
    except:
        print("Failed to save configuration")

def get_config_path():
    # Create 'Config' folder in the app directory
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)
    print("Config directory: ", config_dir)
    
    # Return the full path to the config file
    return config_dir / "config.json"

async def main() -> None:
    """
    The main entry point of the application.

    Establishes connection to MongoDB database and Discord bot.
    Sets all the UI elements and lays them out.
    Provides all the functionality that the UI elements should posses. 

    Returns:
        None 
    """
    # Establish database connection
    db = DbHandler()

    # Create a new Discord bot
    bot = DiscordBot()

    # Start the Discord bot in the background
    bot_task = asyncio.create_task(bot.run())

    # Wait for the bot to be ready
    await bot.wait_until_ready()

    # All the playable games
    games = db.get_list_of_games()

    # Colors
    bg_color = "Black"
    fg_color = "White"
    btn_color = "Green"
    btn_mouseover_color = "DarkGreen"
    btn_size = (7, 0)

    # Fonts
    font = ("Arial", 18)

    # Texts
    result_ui = sg.Text("", text_color=fg_color, background_color=bg_color, font=font)
    last_game_result = db.get_last_spin_string()
    is_last_spin_inserted, _ = db.is_last_spin_inserted()
    last_game_result_ui = sg.Text(
        f"\nLast game result? \n({last_game_result})",
        text_color=fg_color,
        background_color=bg_color,
        font=font,
        key="LAST_GAME",
        visible= not is_last_spin_inserted
    )

    win_lose_msg = sg.Text("", text_color=fg_color, background_color=bg_color, font=font)

    games_ui_texts = []

    for _game in games:
        games_ui_texts.append(sg.Text(
            _game,
            text_color=fg_color,
            font=font,
            background_color=bg_color,
            key=_game
        ))

    # Buttons
    win = sg.Button(
        "W",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size,
        visible=not is_last_spin_inserted
    )
    lose = sg.Button(
        "L",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size,
        visible=not is_last_spin_inserted
    )
    announce_button = sg.Button(
        "ANNOUNCE",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )
    send_reaction_message_button = sg.Button(
        "SEND REACTION",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )
    play_by_reactions_button = sg.Button(
        "PLAY REACTION",
        button_color=btn_color,
        font=font,
        mouseover_colors=btn_mouseover_color,
        size=btn_size
    )

    # Menu definition with "Settings"
    menu_def = [['&Menu', ['&Settings']]]

    # Layout creation
    layout = [
        [sg.Menu(menu_def)],
        [[sg.Text(
            game,
            text_color=fg_color,
            font=font,
            background_color=bg_color,
            key=game
        )] for game in games],
        [result_ui],
        [send_reaction_message_button, play_by_reactions_button, announce_button],
        [last_game_result_ui],
        [win, lose],
        [win_lose_msg]
    ]

    # Applications main window setup
    main_window = sg.Window(
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
        event, _ = main_window.read(timeout=100)

        # Pressing W/L buttons condition
        if event == "W":
            win_lose_msg.update("\nYOU ARE THE BEST")
            db.insert_log_into_database(event)
            change_last_spin_insertion_visibility(main_window, db, visible=False)
            continue
        if event == "L":
            win_lose_msg.update("\nYOU SUCK")
            db.insert_log_into_database(event)
            change_last_spin_insertion_visibility(main_window, db, visible=False)
            continue
        if event == "SEND REACTION":
            rolled_game = None
            message_id = await bot.send_message("Let's spin the wheel of luck! Who's in?")
            continue
        if event == "PLAY REACTION":
            # Check that there is a message already sent in the DC chat
            if message_id is None:
                print("You have to send a reaction message first.")
                continue
            players = await bot.get_reaction_users(message_id)

            # No reaction case
            if not players:
                await bot.send_message("Nobody wants to participate :(")
                continue

            # Get list of games that those players have in common
            is_first_player = True
            for player in players:
                # Inicialize the list of common games by the first player
                if is_first_player:
                    common_games = db.get_list_of_user_games(player)
                    is_first_player = False
                    continue
                # Get current players list of games
                player_games = db.get_list_of_user_games(player)
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
            db.update_last_spin(rolled_game.Get(), players=players)
            # Show insertion
            change_last_spin_insertion_visibility(main_window, db, True)
            continue
        if event == "ANNOUNCE":
            if rolled_game is not None:
                # Call Discord Bot to announce the game that has been rolled
                await bot.send_message(
                    "Going to play " + rolled_game.Get() + ", anyone wanna join in?"
                )
            continue
        if event == "Settings":
            await open_settings_window(font, bg_color, fg_color)
        if event == sg.WIN_CLOSED:
            # Properly shutting down the bot and its loop
            await bot.logout()
            # Wait for the logout operation to end, closing the discord bot thread
            await bot_task
            main_window.close()
            break
        # Yield control back to the event loop
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    # Create an event loop for the main function
    asyncio.run(main())
