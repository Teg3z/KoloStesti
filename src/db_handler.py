"""
db_handler.py

This module contains database handling functions.

Main Functions:
- connect_to_db: Establishes a connection to the MongoDB database.
- get_list_of_games: Retrieves a list of all games from the database.
- get_list_of_user_games: Retrieves a list of games associated with a specific user.
- add_game_to_user_game_list: Adds a game to a user's list of games in the database.
- remove_game_from_user_game_list: Removes a game from a user's list of games in the database.

Dependencies:
- Requires pymongo for MongoDB interactions.
- Requires env_var_loader to load environment variables.
"""

from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_var_loader import get_env_var_value

def connect_to_db():
    """
    Establishes a connection to the MongoDB database.

    Returns:
        pymongo.mongo_client.MongoClient:
            A MongoClient instance connected to the specified database.
    """
    db_connection_string = get_env_var_value("DB_CONNECTION_STRING")
    # Create a new client and connect to the server
    client = MongoClient(db_connection_string, server_api=ServerApi('1'))
    # Connect to database namespace
    return client['WheelOfLuck']

def get_last_spin_string(db):
    """
    Retrieves the whole record of the last spin collection from MongoDB.
    
    Makes the record in a string form that is easily printable for the user,
    so the user can understand it. 

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.

    Returns:
        String: Contains every relevant attribute of the last spin record
            (`last_category`, `last_game`, `last_game_date`) in an easily readable form.
    """
    collection = db['LastSpin']
    entry = collection.find_one()
    formatted_time = entry['last_game_date'].strftime("%d/%m/%Y %H:%M:%S")

    return str(entry['players']) + " - " + entry['last_game'] + \
        " [" + formatted_time + "]"

def update_last_spin(db, game, players):
    """
    Updates the last spin in the MongoDB collection.

    The function takes the current time as the time of the spin.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        game (string): The name of the game that was rolled during the spin.
        players (List): The list of players who participated in the wheel spin.
            (By reacting to the bots Discord message). 

    Returns:
        None
    """
    # Create the time of the spin
    time = datetime.now()

    # Select the correct collection from the DB and create the new data values to enter
    collection = db['LastSpin']
    new_values = { "$set": {
        "last_game": game,
        "last_game_date": time,
        "players": players,
        "is_inserted": False
        }
    }
    # Get the single entry that will be updated
    entry = collection.find_one()
    id_filter = {'_id': entry['_id']}

    collection.update_one(id_filter, new_values)

def is_last_spin_inserted(db):
    """
    Checks whether the last spin in the DB was already inserted or not.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
    Returns:
        tuple: A tuple containing:
            - bool: A boolean indicating whether the last spin was already inserted into the logs.
            - entry (dictionary): The last spin document.
    """
    collection = db['LastSpin']
    entry = collection.find_one()

    if entry["is_inserted"]:
        return True, entry
    return False, entry

def insert_log_into_database(db, result):
    """
    Gets all information from the last spin in the database and inserts
    a new document with the `result` parameter. Only inserts when the last spin
    wasn't already inserted before.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        result (string): The result of the played game. Either "W" or "L" (Win/Lose).

    Returns:
        None
    """
    is_inserted, entry = is_last_spin_inserted(db)
    if not is_inserted:
        new_values = { "$set": {
            "is_inserted": True
            }
        }
        id_filter = {'_id': entry['_id']}
        db['LastSpin'].update_one(id_filter, new_values)
    else:
        return

    collection = db['Logs']
    post = {
        "game_date": entry['last_game_date'],
        "game": entry['last_game'],
        "result": result,
        "players": entry['players']
    }

    collection.insert_one(post)

def get_list_of_games(db):
    """
    Retrieves a list of all games from the MongoDB database in alphabetically sorted order.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.

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

def add_new_player(db, user_name):
    collection = db["Players"]
    new_document = {
        "name": user_name,
        "games": []
        }
    collection.insert_one(new_document)
    return new_document

def get_list_of_user_games(db, user_name):
    """
    Retrieves a list of all games from the MongoDB database in alphabetically sorted order.
    for the specified user.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        user_name (string): Users Dicord name (not server nick).

    Returns:
        List: A list of strings containing all users game names (alphabetically sorted).
    """
    collection = db["Players"]
    user = collection.find_one({"name": user_name})
    if user is None:
        user = add_new_player(db, user_name)
    user_games = user["games"]
    # Sort the games alphabetically
    user_games.sort()
    return user_games

def add_game_to_game_list(db, game):
    """
    Adds a game name to the list of games in the database.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        game (string): A name of the game.

    Returns:
        Bool: Indication whether the game was removed or not.
    """
    collection = db["Games"]

    # Check whether there already is a game with that name
    count = collection.count_documents({"name": game})
    if count != 0:
        return False

    collection.insert_one({"name": game})
    return True

def remove_game_from_game_list(db, game):
    """
    Removes a game name from a list of games in the database.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        game (string): A name of the game.

    Returns:
        Bool: Indication whether the game was removed or not.
    """
    collection = db["Games"]

    # Check whether there already is a game with that name
    count = collection.count_documents({"name": game})
    if count == 0:
        return False

    collection.delete_one({"name": game})
    return True

def add_game_to_user_game_list(db, user_name, game):
    """
    Adds a game name to the users list of games in the database.

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        user_name (string): Users Dicord name (not server nick).
        game (string): A name of the game.

    Returns:
        None
    """
    collection = db["Players"]
    user = collection.find_one({"name": user_name})
    if user is None:
        add_new_player(db, user_name)
    collection.update_one(
        {"name": user_name},
        {"$addToSet": {"games": game}}
    )

def remove_game_from_user_game_list(db, user_name, game):
    """
    Removes a game name from the users list of games in the database.   

    Parameters:
        db (pymongo.mongo_client.MongoClient):
            An instance of a MongoClient connected to the specified database.
        user_name (string): Users Dicord name (not server nick).
        game (string): A name of the game.

    Returns:
        None
    """
    collection = db["Players"]
    user = collection.find_one({"name": user_name})
    if user is None:
        add_new_player(db, user_name)
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
    collection = get_list_of_user_games(db, "tegez")

    # Now you can perform operations on the collection, such as finding all players
    for query in collection:
        print(query)

if __name__ == "__main__":
    main()
