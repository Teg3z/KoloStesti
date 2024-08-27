from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_var_loader import get_env_var_value
import re

# Database connetion
def connect_to_db():
    DB_CONNECTION_STRING = get_env_var_value("DB_CONNECTION_STRING")
    # Create a new client and connect to the server
    client = MongoClient(DB_CONNECTION_STRING, server_api=ServerApi('1'))
    # Connect to database namespace
    return client['WheelOfLuck']

def get_logs():
    # Add LOGS_PATH value into the variables.env file to send logs from that location into MongoDB
    LOGS_PATH = get_env_var_value("LOGS_PATH")

    GTA_LOGS_PATH = LOGS_PATH + "GTARacy.txt"

    return [GTA_LOGS_PATH]

def retrieve_game_data_from_line(line):
        post = {
            "race_name": line,
        }
        return post

def get_list_of_games(db):
    games = []
    collection = db["Games"]

    for query in collection.find():
        games.append(query["name"])

    # Sort the games alphabetically
    games.sort()
    return games

def get_list_of_users_games(db, user_name):
    collection = db["Players"]
    user = collection.find_one({"name": user_name})
    user_games = user["games"]
    # Sort the games alphabetically
    user_games.sort()
    return user_games

def add_game_to_users_games_list(db, user_name, game):
    collection = db["Players"]
    collection.update_one(
        {"name": user_name},
        {"$addToSet": {"games": game}}
    )

def remove_game_from_users_games_list(db, user_name, game):
    collection = db["Players"]
    collection.update_one(
        {"name": user_name},
        {"$pull": {"games": game}}
    )

def get_collection(path):
    match = re.search(r"(Logs.+?)\.txt", path)
    if match:
         captureGroup = match.group(1)    
    return captureGroup

def sent_to_db(json_data, collection):
    collection.insert_one(json_data)

def main():
    db = connect_to_db()
    collection = get_list_of_users_games(db, "tegez")

    # Now you can perform operations on the collection, such as finding all players
    for query in collection:
        print(query)

if __name__ == "__main__":
    main()