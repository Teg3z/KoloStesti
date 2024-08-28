"""
multi_entry_col_parser.py

Re-parses already existing Collection with multiple entries into a single document collection.

Main Functions:
- parse_entries: Establishes a connection to the MongoDB database.
- append_to_array: Retrieves a list of all games from the database.

Dependencies:
- Requires `connect_to_db` from `db_handler` for establishing connection to MongoDB.
"""

from db_handler import connect_to_db

def parse_entries(import_collection, key="race_name"):
    """
    From collection, parses each value of specified key of all documents into a list.

    Parameters:
        import_collection (pymongo.collection.Collection): The MongoDB collection with documents to be parsed.
        key (string): The key name.
    
    Returns:
        Dictionary: A simple dictionary representing a MongoDB document containing the list. 
    """
    tmp_array = []
    for entry in import_collection.find():
        tmp_array.append(entry.get(key))
    # Replace new lines
    tmp_array = [entry.replace('\n', '') for entry in tmp_array]
    document = {
        'list': tmp_array
    }
    return document

def append_to_array(race_name, collection):
    """
    Takes target collection and expected Race Name, appends it to the array, sorts it alphabetically
    and modifies the document, in this manner, via code. Modification CAN BE DONE via MongoDB admin.

    Parameters:
        race_name (string): The name of the race to be added into the collection.
        collection (pymongo.collection.Collection): The MongoDB collection.
    
    Returns:
        None
    """
    collection.update_one({}, {'$push': {'list': {'$each': race_name}}})
    collection.update_one({}, {'$push': {'list': {'$each': [], '$sort': 1}}})

def main():
    """
    The main entry point of the script.

    Defines the `import_collection` from which will the documents be parsed into a list. That list will then
    be inserted into the `export_collection` adn sorted alphabetically.

    Returns:
        None 
    """
    db = connect_to_db()
    import_collection = db['GTARaces']
    export_collection = db['GTARacesPrototype']

    export_collection.insert_one(document=parse_entries(import_collection))

    # Call with empty list will simply sort the array in the document
    append_to_array([], db['GTARacesPrototype'])  # Specify Race names AS A LIST, and the target Collection

if __name__ == '__main__':
    main()
