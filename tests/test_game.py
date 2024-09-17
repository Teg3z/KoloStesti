# tests/test_game.py
import unittest
from src.game import Game

class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        # Arrange
        game_name = "Apex Legends"
        players = ["Player1", "Player2"]
        percentage = 0.9

        # Act
        game = Game(name=game_name, players=players, percentage=percentage)

        # Assert
        self.assertEqual(game.name, game_name)
        self.assertEqual(game.players, players)
        self.assertEqual(game.percentage, percentage)

if __name__ == '__main__':
    unittest.main()
