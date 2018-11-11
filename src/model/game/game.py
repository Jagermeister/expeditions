import random
from .agent.agent import Agent

class Game(object):
    name = None

    def __init__(self, player_count):
        self.player_count = player_count
        self.players = []
        self.turn_ply = 0
        # Ply is a half turn. A full turn is
        # when both players have played.
        self.move_last = None

    def reset(self):
        self.turn_ply = 0
        self.move_last = None

    @staticmethod
    def make_from_state(state):
        pass

    @property
    def state(self):
        return { 'turn_ply': self.turn_ply }

    @property
    def is_terminal(self):
        pass

    def setup(self):
        pass

    def player_add(self, player):
        assert isinstance(player, Agent)
        assert(len(self.players) < self.player_count)
        self.players.append(player)

    @staticmethod
    def moves_available(state):
        pass
    
    def move_play(self, move):
        self.turn_ply += 1
        self.move_last = move

    def move_play_random(self):
        move = random.choice(self.moves_available(self.state))
        self.move_play(move)
        return move

    def reward(self, player_index):
        pass

    @staticmethod
    def state_display(state):
        print('Turn: {}, Last Player: {}'.format(
            state['turn_ply'] // 2,
            1 if state['turn_ply'] % 2 else 2))