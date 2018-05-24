
class Game(object):
    
    def __init__(self, name):
        self.name = name
        self.players = []

    @staticmethod
    def make_from_state(state):
        pass

    @property
    def state(self):
        pass

    @property
    def is_terminal(self):
        pass

    def setup(self):
        pass

    def player_add(self, player):
        self.players.append(player)

    def moves_available(self):
        pass
    
    def move_play(self, move):
        pass