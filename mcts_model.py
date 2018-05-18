from mcts import Node
from player import Player
from card import Card
from model import Model
from copy import deepcopy


class ExpeditionNode(Node):
    # State: deck, playerActiveIndex,
    #   players[0], discard, players[1],
    #   discardLastColor, deckCardCount
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
        super().__init__(state, parent, move)

    def _player(self):
        return self.state[self.player2Index if self.state[self.playerActiveIndex] else self.player1Index]

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

        self.untried_move_count = len(self.moves_discard_deal) + len(self.moves_discard_pull) + len(self.moves_play_deal) + len(self.moves_play_pull)

    def move_untried(self, index):
        a = len(self.moves_discard_deal)
        b = len(self.moves_discard_pull)
        c = len(self.moves_play_deal)
        self.untried_move_count -= 1
        if index < a:
            move = self.moves_discard_deal[index]
            del self.moves_discard_deal[index]
            return ('discard', move)
        elif index < a + b:
            move = self.moves_discard_pull[index - a]
            del self.moves_discard_pull[index - a]
            return ('discard', move)
        elif index < a + b + c:
            move = self.moves_play_deal[index - a - b]
            del self.moves_play_deal[index - a - b]
            return ('play', move)
        else:
            move = self.moves_play_pull[index - a - b - c]
            del self.moves_play_pull[index - a - b - c]
            return ('play', move)

    def advance_by_move(self, move):
        action, (play, pull) = move
        state = deepcopy(self.state)
        if action == 'discard':
            hand, discard, discardLastColor = Model.play_option_discard(
                state[4 if state[self.playerActiveIndex] else 2][Player.handIndex],
                play,
                state[self.discardIndex][play[Card.colorIndex]])
            state[4 if state[self.playerActiveIndex] else 2][Player.handIndex] = hand
            state[self.discardIndex][play[Card.colorIndex]] = discard
            state[self.discardLastColorIndex] = discardLastColor
        else:
            hand, board, boardState = Model.play_option_play(
                state[4 if state[self.playerActiveIndex] else 2][Player.handIndex],
                play,
                state[4 if state[self.playerActiveIndex] else 2][Player.boardStateIndex])
            state[4 if state[self.playerActiveIndex] else 2][Player.handIndex] = hand
            state[4 if state[self.playerActiveIndex] else 2][Player.boardIndex][play[Card.colorIndex]] = board
            state[4 if state[self.playerActiveIndex] else 2][Player.boardStateIndex] = boardState
            state[self.discardLastColorIndex] = None

        if pull == 'd':
            hand, deck = Model.pull_option_deal(
                state[4 if state[self.playerActiveIndex] else 2][Player.handIndex],
                state[self.deckIndex],
                state[self.deckCardCount])
            state[4 if state[self.playerActiveIndex] else 2][Player.handIndex] = hand
            state[self.deckIndex] = deck
            state[self.deckCardCount] -= 1
        else:
            hand, discard = Model.pull_option_pull(
                state[4 if state[self.playerActiveIndex] else 2][Player.handIndex],
                state[self.discardIndex][pull],
                pull
            )
            state[4 if state[self.playerActiveIndex] else 2][Player.handIndex] = hand
            state[self.discardIndex][pull] = discard
        
        state[self.playerActiveIndex] = 0 if state[self.playerActiveIndex] else 0
        return state

    def advance_to_terminal(self):
        #From state, play random until end
        terminalModel = Model.make_from_state(self.state)
        while terminalModel.cardsInDeckCount and terminalModel.winner is None:
            terminalModel.play_random_turn()

        self.is_terminal = True
        self.terminal_reward = terminalModel.winner