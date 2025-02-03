import sys
import os
import unittest

# Get the absolute path of the 'src' directory and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from player import Player

class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        # Arrange
        name = "Player1"
        games = ["Apex Legends", "CS:GO"]

        # Act
        player = Player(name=name, games=games)

        # Assert
        self.assertEqual(player.name, name)
        self.assertEqual(player.games, games)

if __name__ == '__main__':
    unittest.main()
