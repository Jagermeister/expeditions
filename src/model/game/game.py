from .agent.agent import Agent

class Game(object):

    def __init__(self, name, player_count):
        self.name = name
        self.player_count = player_count
        self.players = []
        self.turn_ply = 0

    @staticmethod
    def make_from_state(state):
        pass

    @property
    def state(self):
        return {
            'turn_ply': self.turn_ply
        }

    @property
    def is_terminal(self):
        pass

    def setup(self):
        pass

    def player_add(self, player):
        assert isinstance(player, Agent)
        assert(len(self.players) < self.player_count)
        self.players.append(player)

    def moves_available(self):
        pass
    
    def move_play(self, move):
        self.turn_ply += 1

    def reward(self, player_index):
        pass

    @staticmethod
    def state_display(state):
        print('Turn: {}, Last Player: {}'.format(
            state['turn_ply'] // 2,
            1 if state['turn_ply'] % 2 else 2))