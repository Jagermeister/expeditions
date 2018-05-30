import random
from copy import deepcopy

from ..game import Game


class TTTGame(Game):

    def __init__(self, board=[0] * 9):
        super().__init__('Tic Tac Toe', 2)
        self.board = board

    @staticmethod
    def make_from_state(state):
        state = deepcopy(state)
        return TTTGame(state['board'])

    @property
    def state(self):
        parentState = super().state
        parentState['board'] = self.board
        return parentState

    @property
    def is_terminal(self):
        if 0 not in self.board:
            return True
        for (x, y, z) in [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]:
            if 0 != self.board[x] == self.board[y] == self.board[z]:
                return True
        return False

    @staticmethod
    def moves_available(state):
        board = state['board']
        return [i for i, b in enumerate(board) if b == 0]

    @staticmethod
    def move_play_simulate(board, move):
        board[move] = -1 if sum(board) else 1
        return board

    def move_play(self, move):
        assert(self.board[move] == 0 and move >= 0 and move <= len(self.board))
        super().move_play(move)
        self.board[move] = -1 if sum(self.board) else 1

    def move_play_random(self):
        move = random.choice(self.moves_available(self.state))
        self.move_play(move)
        return move

    def reward(self):
        for (x, y, z) in [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]:
            if self.board[x] == self.board[y] == self.board[z]:
                return 1
        if not len(self.moves_available(self.state)): return 0.5

    @staticmethod
    def state_display(state):
        super(TTTGame, TTTGame).state_display(state)
        print('\t', end='')
        for i, c in enumerate(state['board']):
            print('X' if c == 1 else ('O' if c == -1 else '?'), end='')
            if (i + 1) % 3 == 0:
                print('\n\r', end='' if i == len(state['board']) - 1 else '\t')