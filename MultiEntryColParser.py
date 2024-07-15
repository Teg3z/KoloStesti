# @author R4tmax
# Last edit on: 26.06.2023
# re-parses already existing Collection with multiple entries into a single document collection

# import block
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Configure DB namespace
uri = "mongodb+srv://WOFadmin:TRqz3dHcnAbQataY@wheelofluck.tqghhhz.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# connect to database namespace
db = client['WheelOfLuck']


# takes input collection as argument
# parses each document key - value pair into a list
# returns the values as a simple list
def parse_entries(import_collection):
    tmp_array = []
    for entry in import_collection.find():
        tmp_array.append(entry.get('race_name'))  # specify the expected key of the attribute
    tmp_array = [entry.replace('\n', '') for entry in tmp_array]
    document = {
        'race_list': tmp_array
    }

    return document


# Takes target collection and expected Race Name as argument,
# appends it to the array, sorts it alphabetically
# and modifies the document, in this manner, via code.
# Modification CAN BE DONE via MongoDB admin
def append_to_array(race_name, collection):
    collection.update_one({}, {'$push': {'race_list': {'$each': race_name}}})
    collection.update_one({}, {'$push': {'race_list': {'$each': [], '$sort': 1}}})


def main():
    # import_collection = db['GTARaces']  # specify the source collection with redundant data
    # export_collection = db['GTARacesPrototype']  # specify the expected location of the new data

    # export_collection.insert_one(document=parseEntries(import_collection))

    # call with empty list will simply sort the array in the document
    append_to_array([], db['GTARacesPrototype'])  # Specify Race names AS A LIST, and the target Collection


if __name__ == '__main__':
    main()
