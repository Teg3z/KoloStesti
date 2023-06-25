from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import re

CESTA_LOGY = r"REPLACED_PATH\KoloStesti\\"

CESTA_RACE = CESTA_LOGY + "GTARacy.txt"

list_logu = [CESTA_RACE]

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
    

def sendToMongoDB(json_data,collection):
    collection.insert_one(json_data)

def main():
    #try:
    for log in list_logu:
        soubor = open(log, "rt")
        line = soubor.readline()
        while line:
            # ziskej data z line
            json_data = retrieveGameDataFromLine(line)
            #collection = $najdi kollekci podle Logu
            collection = db['GTARaces']
            sendToMongoDB(json_data, collection)
            line = soubor.readline()
        soubor.close()
    #except Exception as chybaNevimPicoVcem:
    #    print("Chyba: " + str(chybaNevimPicoVcem))
    #    exit()


if __name__ == "__main__":
    main()