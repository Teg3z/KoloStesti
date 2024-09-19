# tests/test_game.py
import unittest
from src.player import Player

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
