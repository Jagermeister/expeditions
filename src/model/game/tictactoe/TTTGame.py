from ..game import Game

class TTTGame(Game):

    def __init__(self, board = [0] * 9):
        super().__init__('Tic Tac Toe')
        self.board = board

    @staticmethod
    def make_from_state(state):
        return TTTGame(state.board)

    @property
    def state(self):
        return {'board': self.board}

    @property
    def is_terminal(self):
        return 0 not in self.board

    def moves_available(self):
        return [i for i, b in enumerate(self.board) if b == 0]

    def move_play(self, move):
        assert(self.board[move] == 0 and move >= 0 and move <= len(self.board))
        self.board[move] = -1 if sum(self.board) else 1