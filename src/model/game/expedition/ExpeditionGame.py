from ..game import Game

from random import randrange
from copy import deepcopy

from .config import Config
from .card import Card
from .deck import Deck
from .player import Player
Config = Config()

class ExpeditionGame(Game):
    name = 'Expeditions'
    player_count = 2

    def __init__(self):
        super().__init__()
        self.deck = 0b0
        # Binary representation of the cards
        self.cardsInDeckCount = 0
        self.discard = []
        # Per color list of card values
        self.playerActiveIndex = 0
        # Index of player who will act next
        self.discardLastColor = None
        # Color that was discarded this Ply which
        # cannot be pulled back by the player
        self.winner = None
        # Query end result

    def reset(self):
        super().reset()
        self.deck = 0b0
        self.cardsInDeckCount = 0
        self.discard = []
        self.playerActiveIndex = 0
        self.discardLastColor = None
        self.winner = None

    @staticmethod
    def make_from_state(state, replaceOpponent=True):
        state = deepcopy(state)
        m = ExpeditionGame()
        m.deck = state[0]
        m.playerActiveIndex = state[1]
        m.players = [
            state[2],
            state[4]
        ]
        m.cardsInDeckCount = state[6]
        if replaceOpponent:
            hand = []
            for c in m.players[m.playerActiveIndex].player[Player.handIndex]:
                m.deck = Card.add(m.deck, Card.to_index(c))
                m.cardsInDeckCount += 1

            for _ in range(Config.cardsInHandCount):
                m.deck, card = Deck.cardChoice(m.deck, m.cardsInDeckCount)
                hand.append(card)
                m.cardsInDeckCount -= 1

            m.players[m.playerActiveIndex].player[Player.handIndex] = hand
        m.discard = state[3]
        m.discardLastColor = state[5]
        return m

    def __str__(self):
        print('\tlen(deck) =', self.cardsInDeckCount)
        print('\tP1.Hand', self.players[0].player[Player.handIndex])
        print('\tP1.Board', self.players[0].player[Player.boardIndex], bin(self.players[0].player[Player.boardStateIndex]))
        print('\tDiscard', self.discard)
        print('\tP2.Board', self.players[1].player[Player.boardIndex], bin(self.players[1].player[Player.boardStateIndex]))
        print('\tP2.Hand', self.players[1].player[Player.handIndex])
        print('\tScore:',
            Player.board_score(self.players[0].player[Player.boardStateIndex]),
            Player.board_score(self.players[1].player[Player.boardStateIndex]))
        return ""

    def player(self):
        return self.players[self.playerActiveIndex].player

    @staticmethod
    def pull_option_deal(hand, deck, cardCount):        
        deck, card = Deck.cardChoice(
            deck, cardCount
        )
        hand.append(card)
        return (hand, deck)

    def card_deal(self):
        # Deck to Hand
        #self.deck, card, self.cardsInDeckCount = Deck.cardChoice(
        #    self.deck, self.cardsInDeckCount)
        #hand = self.player()[Player.handIndex]
        #hand.append(card)
        self.player()[Player.handIndex], self.deck = ExpeditionGame.pull_option_deal(
            self.player()[Player.handIndex],
            self.deck,
            self.cardsInDeckCount
        )
        self.cardsInDeckCount -= 1
        self.playerActiveIndex = 0 if self.playerActiveIndex else 1

    def setup(self):
        self.cardsInDeckCount = Config.cardsInDeckCount
        self.deck = Deck.create(self.cardsInDeckCount)
        self.discard = [[] for _ in range(Config.colorCount)]
        #self.players = [
        #    Player.create(),
        #    Player.create()
        #]
        # Deal starting hand
        for _ in range(Config.cardsInHandCount * len(self.players)):
            self.card_deal()

 
    @staticmethod
    def play_option_discard(hand, card, discard):
        hand.remove(card)
        discard.append(card[Card.valueIndex])
        return (hand, discard, card[Card.colorIndex])

    def card_discard(self, card):
        # Hand to Discard
        #self.player()[Player.handIndex].remove(card)
        #self.discard[card[Card.colorIndex]].append(card[Card.valueIndex])
        #self.discardLastColor = card[Card.colorIndex]
        hand = self.player()[Player.handIndex]
        discard = self.discard[card[Card.colorIndex]]
        hand, discard, discardColor = ExpeditionGame.play_option_discard(hand, card, discard)
        self.player()[Player.handIndex] = hand
        self.discard[card[Card.colorIndex]] = discard
        self.discardLastColor = discardColor

    @staticmethod
    def play_option_play(hand, card, boardState):
        hand.remove(card)
        color, value = card
        boardState |= 1 << (value + Config.cardsInColorCount * color)
        return (hand, value, boardState)

    def card_play(self, card):
        # Hand to Board
        #color, value = card
        #p[Player.handIndex].remove(card)
        #p[Player.boardIndex][color] = value
        #p[Player.boardStateIndex] |= 1 << (value + Config.cardsInColorCount * color)
        p = self.player()
        color, _ = card
        hand, board, boardState = ExpeditionGame.play_option_play(
            p[Player.handIndex],
            card,
            p[Player.boardStateIndex])
        p[Player.handIndex] = hand
        p[Player.boardIndex][color] = board
        p[Player.boardStateIndex] = boardState
        self.discardLastColor = None

    @staticmethod
    def pull_option_pull(hand, discard, color):
        hand.append((color, discard.pop()))
        return (hand, discard)

    def card_pull(self, color):
        # Discard to Hand
        #p[Player.handIndex].append((color, self.discard[color].pop()))
        p = self.player()
        hand, discard = ExpeditionGame.pull_option_pull(
            p[Player.handIndex],
            self.discard[color],
            color
        )
        p[Player.handIndex] = hand
        self.discard[color] = discard
        self.playerActiveIndex = 0 if self.playerActiveIndex else 1

    def play_move(self, move):
        self.turnPly += 1
        action, (play, pull) = move
        if action == 'discard':
            self.card_discard(play)
        else:
            self.card_play(play)

        if pull == 'd':
            self.card_deal()
        else:
            self.card_pull(pull)

        # 3. Winner?
        if not self.cardsInDeckCount:
            p1Score = Player.board_score(self.players[0].player[Player.boardStateIndex])
            p2Score = Player.board_score(self.players[1].player[Player.boardStateIndex])
            self.winner = 1 if p1Score > p2Score else (-1 if p2Score > p1Score else 0)

    def play_random_turn(self):
        self.turnPly += 1
        p = self.player()
        # 1. PLAY: From hand to (board or discard)
        o = Player.play_options(p[Player.handIndex], p[Player.boardIndex])
        a = randrange(0, Config.cardsInHandCount + len(o))
        if a < Config.cardsInHandCount:
            #self.card_discard(p[Player.handIndex][a])
            play = 'discard'
            card = p[Player.handIndex].pop(a)
            color, value = card
            self.discard[color].append(value)
            self.discardLastColor = color
        else:
            #self.card_play(o[a-Config.cardsInHandCount])
            play = 'play'
            card = o[a-Config.cardsInHandCount]
            p[Player.handIndex].remove(card)
            color, value = card
            p[Player.boardIndex][color] = value
            p[Player.boardStateIndex] |= 1 << (value + 12 * color)

        # 2. PULL: From (deck or discard) to hand
        o = Player.pull_options(self.discard, self.discardLastColor)
        a = randrange(0, 1 + len(o))
        if o and a:
            #self.card_pull(o[a-1])
            color = o[a-1]
            pull = color
            card = (color, self.discard[color].pop())
            p[Player.handIndex].append(card)
        else:
            #self.card_deal()
            pull = 'd'
            self.deck, card = Deck.cardChoice(self.deck, self.cardsInDeckCount)
            p[Player.handIndex].append(card)
            self.cardsInDeckCount -= 1

        move = (play, (card, pull))
        if self.turnPly > Config.turnsUntilForcedLoss:
            self.winner = -1
            return move

        # 3. Winner?
        if not self.cardsInDeckCount:
            p1Score = Player.board_score(self.players[0].player[Player.boardStateIndex])
            p2Score = Player.board_score(self.players[1].player[Player.boardStateIndex])
            self.winner = 1 if p1Score > p2Score else (-1 if p2Score > p1Score else 0)
            return move

        self.playerActiveIndex = 0 if self.playerActiveIndex else 1
        return move

    @property
    def state(self):
        return [
            self.deck,
            self.playerActiveIndex,
            self.players[0].player,
            self.discard,
            self.players[1].player,
            self.discardLastColor,
            self.cardsInDeckCount
        ]

    @property
    def is_terminal(self):
        return not self.cardsInDeckCount

    @staticmethod
    def moves_available(state):
        pass

    def reward(self):
        pass