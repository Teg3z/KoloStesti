"""
db_handler.py

This module contains database handling functions.

Functions:
- connect_to_db: Establishes a connection to the MongoDB database.
- get_list_of_games: Retrieves a list of all games from the database.
- get_list_of_users_games: Retrieves a list of games associated with a specific user.
- add_game_to_users_games_list: Adds a game to a user's list of games in the database.
- remove_game_from_users_games_list: Removes a game from a user's list of games in the database.

Dependencies:
- Requires pymongo for MongoDB interactions.
- Requires env_var_loader to load environment variables.
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_var_loader import get_env_var_value

def connect_to_db():
    """
    Establishes a connection to the MongoDB database.

    Returns:
        MongoClient: A MongoClient instance connected to the specified database.
    """
    db_connection_string = get_env_var_value("DB_CONNECTION_STRING")
    # Create a new client and connect to the server
    client = MongoClient(db_connection_string, server_api=ServerApi('1'))
    # Connect to database namespace
    return client['WheelOfLuck']

def get_logs():
    """
    Retrieves a logs path to the GTA races in the local environment.

    Returns:
        List: A list of strings representing names of the GTA races from local logs.
    """
    # Add logs_path value into the variables.env file to send logs from that location into MongoDB
    logs_path = get_env_var_value("LOGS_PATH")

    gta_logs_path = logs_path + "GTARacy.txt"

    return [gta_logs_path]

def get_list_of_games(db):
    """
    Retrieves a list of all games from the MongoDB database in alphabetically sorted order.

    Parameters:
        db (MongoClient): An instance of a MongoClient connected to the specified database

    Returns:
        List: A list of strings containing all game names (alphabetically sorted).
    """
    games = []
    collection = db["Games"]

    for query in collection.find():
        games.append(query["name"])

    # Sort the games alphabetically
    games.sort()
    return games

def get_list_of_users_games(db, user_name):
    """
    Retrieves a list of all games from the MongoDB database in alphabetically sorted order
    for the specified user.

    Parameters:
        db (MongoClient): An instance of a MongoClient connected to the specified database
        user_name (string): Users Dicord name (not server nick)

    Returns:
        List: A list of strings containing all users game names (alphabetically sorted).
    """
    collection = db["Players"]
    user = collection.find_one({"name": user_name})
    user_games = user["games"]
    # Sort the games alphabetically
    user_games.sort()
    return user_games

def add_game_to_users_games_list(db, user_name, game):
    """
    Adds a game name to the users list of games in the database.

    Parameters:
        db (MongoClient): An instance of a MongoClient connected to the specified database
        user_name (string): Users Dicord name (not server nick)
        game (string): A name of the game

    Returns:
        None
    """
    collection = db["Players"]
    collection.update_one(
        {"name": user_name},
        {"$addToSet": {"games": game}}
    )

def remove_game_from_users_games_list(db, user_name, game):
    """
    Removes a game name from the users list of games in the database.   

    Parameters:
        db (MongoClient): An instance of a MongoClient connected to the specified database
        user_name (string): Users Dicord name (not server nick)
        game (string): A name of the game

    Returns:
        None
    """
    collection = db["Players"]
    collection.update_one(
        {"name": user_name},
        {"$pull": {"games": game}}
    )

def main():
    """
    The main entry point of the script.

    Only used for testing this module.

    Returns:
        None 
    """
    db = connect_to_db()
    collection = get_list_of_users_games(db, "tegez")

    # Now you can perform operations on the collection, such as finding all players
    for query in collection:
        print(query)

if __name__ == "__main__":
    main()
