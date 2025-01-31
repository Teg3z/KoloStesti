"""
player.py

Module containing the definition of the Player class.

"""

class Player:
    """
    This class represents an actual player.
    """

    def __init__(self, name, games):
        """
        Initializes the Player class.

        Parameters:
            name (string): The name of the player.
            games (List): A list of strings containing every game name
                the player is willing to play.
        """
        self.name = name
        self.games = games
