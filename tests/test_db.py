import sys
import os

# Get the absolute path of the 'src' directory and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from datetime import datetime
from src.db_handler import connect_to_db, insert_log_into_database

class TestDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.db = connect_to_db("WheelOfLuckTest")
        self.collection = self.db['LastSpin']
        self.logs_collection = self.db['Logs']

    def tearDown(self):
        self.collection.delete_many({})
        self.logs_collection.delete_many({})

    def test_insert_log(self):
        # Insert a test document in LastSpin
        test_entry = {
            "last_game": "Apex Legends",
            "last_game_date": datetime.now(),
            "players": ["player1", "player2"],
            "is_inserted": False
        }
        self.collection.insert_one(test_entry)

        # Call the function to insert log
        filter_id = insert_log_into_database(self.db, "W")

        # Check if the document was inserted into Logs
        inserted_log = self.logs_collection.find_one(filter_id)
        self.assertIsNotNone(inserted_log)
        self.assertEqual(inserted_log["result"], "W")

if __name__ == '__main__':
    unittest.main()
