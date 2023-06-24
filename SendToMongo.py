from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import re

CESTA_LOGY = r"REPLACED_PATH\KoloStesti\\"

CESTA_LOGY_DK = CESTA_LOGY + "LogsDK.txt"
CESTA_LOGY_DF = CESTA_LOGY + "LogsDF.txt"
CESTA_LOGY_DFK = CESTA_LOGY + "LogsDFK.txt"
CESTA_LOGY_D = CESTA_LOGY + "LogsD.txt"
CESTA_LOGY_DFKM = CESTA_LOGY + "LogsDFKM.txt"
CESTA_LOGY_DKKA = CESTA_LOGY + "LogsDKKA.txt"

list_logu = [CESTA_LOGY_DF, CESTA_LOGY_DFK, CESTA_LOGY_DFKM, CESTA_LOGY_DK, CESTA_LOGY_DKKA]

# pripoj se k DB
# databaze
uri = "REPLACED_DB_CONNECTION_STRING"
# # Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# connect to database namespace
db = client['WheelOfLuck']

def retrieveGameDataFromLine(line):
        document_entries = line.strip().split(' ')
        game_date = document_entries[0]
        game_result = document_entries[len(document_entries) - 1]
        document_entries.pop()
        document_entries.pop(0)
        game_name = ""
        for entry in document_entries:
            game_name += entry + " "
        game_name.strip()

        post = {
            "game_date": game_date,
            "game": game_name,
            "result": game_result
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
            collection = db[getCollection(log)]
            sendToMongoDB(json_data, collection)
            line = soubor.readline()
        soubor.close()
    #except Exception as chybaNevimPicoVcem:
    #    print("Chyba: " + str(chybaNevimPicoVcem))
    #    exit()


if __name__ == "__main__":
    main()