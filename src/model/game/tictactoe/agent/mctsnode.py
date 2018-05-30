import copy

from ...agent.mctsnode import Node
from ..TTTGame import TTTGame

class TTTNode(Node):
    def __init__(self, state, parent=None, move=None):
        self.moves = []
        super().__init__(state, parent, move)

    def child_add(self, state, move):
        self.children.append(TTTNode(state, self, move))

    def moves_generate(self):
        board = self.state['board']
        if 0 not in board:
            self.terminal_reward = 1
            self.is_terminal = True
            return
        for (x, y, z) in [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]:
            if 0 != board[x] == board[y] == board[z]:
                self.terminal_reward = 1
                self.is_terminal = True
                return

        self.moves = TTTGame.moves_available(self.state)
        self.untried_move_count = len(self.moves)

    def move_untried(self, index):
        self.untried_move_count -= 1
        move = self.moves[index]
        del self.moves[index]
        return move

    def advance_by_move(self, move):
        return { 'board': TTTGame.move_play_simulate(self.state['board'][:], move) }

    def advance_to_terminal(self):
        #print(len([b for b in self.state['board'] if b != 0]), self.state)
        terminalM = TTTGame.make_from_state(self.state)
        while not terminalM.is_terminal:
            terminalM.move_play_random()

        self.is_terminal = True
        #TTTGame.state_display(terminalM.state)
        #print('player', 1 if sum(self.state['board']) else 0, 'result', terminalM.reward(0 if sum(self.state['board']) else 1))
        self.terminal_reward = terminalM.reward()