import random
from copy import deepcopy

from ..game import Game

class GuessGame(Game):
    name = 'Deuce to Seven - Triple Draw'
    player_count = 6

    def __init__(self):
        super().__init__()