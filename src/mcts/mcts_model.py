""" Concrete Expedition implementation of Node """

from copy import deepcopy

from src.mcts.node import Node
from src.model.player import Player
from src.model.card import Card
from src.model.model import Expedition as M


class ExpeditionNode(Node):
    """ State: deck, playerActiveIndex,
        players[0], discard, players[1],
        discardLastColor, deckCardCount
    """
    deckIndex = 0
    playerActiveIndex = 1
    player1Index = 2
    discardIndex = 3
    player2Index = 4
    discardLastColorIndex = 5
    deckCardCount = 6

    def __init__(self, state, parent=None, move=None):
        self.moves_discard_deal = []
        self.moves_discard_pull = []
        self.moves_play_deal = []
        self.moves_play_pull = []
        self.terminal_reward = None
        super().__init__(state, parent, move)

    def _player(self):
        player_active = self.state[self.playerActiveIndex]
        return self.state[self.player2Index if player_active else self.player1Index]

    def _discard(self):
        return self.state[self.discardIndex]

    def child_add(self, state, move):
        self.children.append(ExpeditionNode(state, self, move))

    def moves_generate(self):
        # From state, determine possible moves
        if not self.state[self.deckCardCount]:
            self.terminal_reward = 0
            self.is_terminal = True
            return

        p = self._player()
        hand = p[Player.handIndex]
        plays = Player.play_options(hand, p[Player.boardIndex])
        pulls = Player.pull_options(self.state[self.discardIndex])
        for c in hand:
            self.moves_discard_deal.append((c, 'd'))
            for pull in pulls:
                self.moves_discard_pull.append((c, pull))

        for play in plays:
            self.moves_play_deal.append((play, 'd'))
            for pull in pulls:
                self.moves_play_pull.append((play, pull))

        self.untried_move_count = len(self.moves_discard_deal) +\
            len(self.moves_discard_pull) +\
            len(self.moves_play_deal) +\
            len(self.moves_play_pull)

    def move_untried(self, index):
        a = len(self.moves_discard_deal)
        b = len(self.moves_discard_pull)
        c = len(self.moves_play_deal)
        self.untried_move_count -= 1
        if index < a:
            move = self.moves_discard_deal[index]
            del self.moves_discard_deal[index]
            return ('discard', move)

        if index < a + b:
            move = self.moves_discard_pull[index - a]
            del self.moves_discard_pull[index - a]
            return ('discard', move)

        if index < a + b + c:
            move = self.moves_play_deal[index - a - b]
            del self.moves_play_deal[index - a - b]
            return ('play', move)

        move = self.moves_play_pull[index - a - b - c]
        del self.moves_play_pull[index - a - b - c]
        return ('play', move)

    def advance_by_move(self, move):
        action, (play, pull) = move
        state = deepcopy(self.state)
        player_active = 4 if state[self.playerActiveIndex] else 2
        if action == 'discard':
            hand, discard, discard_last_color = M.play_option_discard(
                state[player_active][Player.handIndex],
                play,
                state[self.discardIndex][play[Card.colorIndex]])
            state[player_active][Player.handIndex] = hand
            state[self.discardIndex][play[Card.colorIndex]] = discard
            state[self.discardLastColorIndex] = discard_last_color
        else:
            hand, board, board_state = M.play_option_play(
                state[player_active][Player.handIndex],
                play,
                state[player_active][Player.boardStateIndex])
            state[player_active][Player.handIndex] = hand
            state[player_active][Player.boardIndex][play[Card.colorIndex]] = board
            state[player_active][Player.boardStateIndex] = board_state
            state[self.discardLastColorIndex] = None

        if pull == 'd':
            hand, deck = M.pull_option_deal(
                state[player_active][Player.handIndex],
                state[self.deckIndex],
                state[self.deckCardCount])
            state[player_active][Player.handIndex] = hand
            state[self.deckIndex] = deck
            state[self.deckCardCount] -= 1
        else:
            hand, discard = M.pull_option_pull(
                state[player_active][Player.handIndex],
                state[self.discardIndex][pull],
                pull
            )
            state[player_active][Player.handIndex] = hand
            state[self.discardIndex][pull] = discard

        state[self.playerActiveIndex] = 0 if state[self.playerActiveIndex] else 0
        return state

    def advance_to_terminal(self):
        """ From state, play random until end """
        terminal_move = M.make_from_state(self.state)
        while terminal_move.cardsInDeckCount and terminal_move.winner is None:
            terminal_move.play_random_turn()

        self.is_terminal = True
        self.terminal_reward = terminal_move.winner
