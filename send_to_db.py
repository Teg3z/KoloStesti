from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import re

LOGS_PATH = r"REPLACED_PATH\\"

GTA_LOGS_PATH = LOGS_PATH + "GTARacy.txt"

logs = [GTA_LOGS_PATH]

# pripoj se k DB
# databaze
uri = "REPLACED_DB_CONNECTION_STRING"
# # Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# connect to database namespace
db = client['WheelOfLuck']

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
    #try:
    for log in logs:
        file = open(log, "rt")
        line = file.readline()
        while line:
            json_data = retrieveGameDataFromLine(line)
            collection = db['GTARaces']
            sent_to_db(json_data, collection)
            line = file.readline()
        file.close()
    #except Exception as chybaNevimPicoVcem:
    #    print("Chyba: " + str(chybaNevimPicoVcem))
    #    exit()

if __name__ == "__main__":
    main()