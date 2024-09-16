"""
game.py

Module containing the definition of the Game class.

"""

class Game:
    """
    This class represents a game instance.
    """

    def __init__(self, name, players, percentage):
        """
        Initializes the Game class.

        Parameters:
            name (string): The name of the game.
            players (List): A list of strings containing every possible variation
                of players for this game.
            percentage (int): A number containing the satisfaction value
                when the game is selected to be played (0-1).
        """
        self.name = name
        self.players = players
        self.percentage = percentage
