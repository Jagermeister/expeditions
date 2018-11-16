import random
from copy import deepcopy

from ..game import Game

class GuessGame(Game):
    name = 'Guess The Number'
    player_count = 1

    def __init__(self):
        super().__init__()
        self.secret_number_min = 0
        self.secret_number_max = 64
        self.guess_count_max = 6
        self.reset()

    def secret_number_valid(self, secret_number):
        assert(secret_number == None or isinstance(secret_number, int))
        return secret_number and secret_number > self.secret_number_min and secret_number < self.secret_number_max

    def reset(self):
        super().reset()
        self.secret_number = random.randint(self.secret_number_min, self.secret_number_max)
        self.guess_number_lower_limit = self.secret_number_min
        self.guess_number_upper_limit = self.secret_number_max

    @staticmethod
    def make_from_state(state):
        state = deepcopy(state)
        return state

    @property
    def state(self):
        parentState = super().state
        parentState['secret_number'] = self.secret_number
        parentState['guess_number_lower_limit'] = self.guess_number_lower_limit
        parentState['guess_number_upper_limit'] = self.guess_number_upper_limit
        return parentState

    @property
    def is_terminal(self):
        return self.turn_ply > self.guess_count_max or self.move_last == self.secret_number

    @staticmethod
    def moves_available(state):
        lower = state['guess_number_lower_limit']
        upper = state['guess_number_upper_limit']
        return [i for i in range(lower, upper)]

    def move_play(self, move):
        assert(isinstance(move, int))
        super().move_play(move)
        if self.secret_number <= move and move < self.guess_number_upper_limit:
            self.guess_number_upper_limit = move
        
        if self.secret_number >= move and move > self.guess_number_lower_limit:
            self.guess_number_lower_limit = move

    def reward(self):
        return int(self.turn_ply <= self.guess_count_max)

    def state_display(self, state=None):
        if not state:
            state = self.state
        #super().state_display(state)
        turn_ply = state['turn_ply']
        lower = state['guess_number_lower_limit']
        upper = state['guess_number_upper_limit']

        print('You have made {} guesses out of {}.'.format(turn_ply, 6))
        if lower == upper:
            print('You found the secret number {}!'.format(lower))
        else:
            print('You have narrowed down the number between {} and {}'.format(lower, upper))