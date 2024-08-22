from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from env_var_loader import get_env_var_value
import re

# Add LOGS_PATH value into the variables.env file to send logs from that location into MongoDB
LOGS_PATH = get_env_var_value("LOGS_PATH")

GTA_LOGS_PATH = LOGS_PATH + "GTARacy.txt"

logs = [GTA_LOGS_PATH]

# Database connetion
def connect_to_db():
    DB_CONNECTION_STRING = get_env_var_value("DB_CONNECTION_STRING")
    # Create a new client and connect to the server
    client = MongoClient(DB_CONNECTION_STRING, server_api=ServerApi('1'))
    # Connect to database namespace
    return client['WheelOfLuck']

def retrieveGameDataFromLine(line):
        post = {
            "race_name": line,
        }
        return post

def getCollection(path):
    match = re.search(r"(Logs.+?)\.txt", path)
    if match:
         captureGroup = match.group(1)    
    return captureGroup

def sent_to_db(json_data, collection):
    collection.insert_one(json_data)

def main():
    db = connect_to_db()

    for log in logs:
        file = open(log, "rt")
        line = file.readline()
        while line:
            json_data = retrieveGameDataFromLine(line)
            collection = db['GTARaces']
            sent_to_db(json_data, collection)
            line = file.readline()
        file.close()

if __name__ == "__main__":
    main()