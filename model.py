from config import Config
from card import Card
from deck import Deck
from player import Player
import random
import copy
Config = Config()

class Model:
    def __init__(self):
        self.deck = 0b0
        # Binary representation of the cards
        self.cardsInDeckCount = 0
        self.discard = []
        # Per color list of card values
        self.players = []
        self.playerActiveIndex = 0
        # Index of player who will next
        self.turnPly = 0
        # Ply is a half turn. A full turn is
        # when both players have played.
        self.discardLastColor = None
        # Color that was discarded this Ply which
        # cannot be pulled back by the player
        self.winner = None
        # Query end result

    @staticmethod
    def make_from_state(state, replaceOpponent=True):
        state = copy.deepcopy(state)
        m = Model()
        m.deck = state[0]
        m.playerActiveIndex = state[1]
        m.players = [
            state[2],
            state[4]
        ]
        m.cardsInDeckCount = state[6]
        if replaceOpponent:
            hand = []
            for c in m.players[m.playerActiveIndex][Player.handIndex]:
                m.deck = Card.add(m.deck, Card.to_index(c))
                m.cardsInDeckCount += 1

            for _ in range(8):
                m.deck, card = Deck.cardChoice(m.deck, m.cardsInDeckCount)
                hand.append(card)
                m.cardsInDeckCount -= 1

            m.players[m.playerActiveIndex][Player.handIndex] = hand
        m.discard = state[3]
        m.discardLastColor = state[5]
        return m

    def __str__(self):
        print('Deck', self.cardsInDeckCount, self.playerActiveIndex)#, bin(self.deck))
        print('Player1.Hand', self.players[0][Player.handIndex])
        print('Player1.Board', self.players[0][Player.boardIndex], bin(self.players[0][Player.boardStateIndex]))
        print('Discard', self.discard)
        print('Player2.Board', self.players[1][Player.boardIndex], bin(self.players[1][Player.boardStateIndex]))
        print('Player2.Hand', self.players[1][Player.handIndex])
        print('Score:',
            Player.board_score(self.players[0][Player.boardStateIndex]),
            Player.board_score(self.players[1][Player.boardStateIndex]))
        return ""

    def player(self):
        # Active Player
        return self.players[self.playerActiveIndex]

    @staticmethod
    def pull_option_deal(hand, deck, cardCount):        
        deck, card = Deck.cardChoice(
            deck, cardCount
        )
        hand.append(card)
        return (hand, deck)

    def card_deal(self):
        # Deck to Hand
        self.player()[Player.handIndex], self.deck = Model.pull_option_deal(
            self.player()[Player.handIndex],
            self.deck,
            self.cardsInDeckCount
        )
        self.cardsInDeckCount -= 1
        #self.deck, card, self.cardsInDeckCount = Deck.cardChoice(
        #    self.deck, self.cardsInDeckCount)
        #hand = self.player()[Player.handIndex]
        #hand.append(card)
        self.playerActiveIndex = 0 if self.playerActiveIndex else 1

    def setup(self):
        # Deck of cards
        self.cardsInDeckCount = Config.cardsInDeckCount
        self.deck = Deck.create(self.cardsInDeckCount)
        # Discard pile
        self.discard = [[] for _ in range(Config.colorCount)]
        # Players
        self.players = [
            Player.create(),
            Player.create()
        ]
        # Deal starting hand
        for _ in range(Config.cardsInHandCount * len(self.players)):
            self.card_deal()

    @staticmethod
    def play_option_discard(hand, card, discard):
        #print(hand, card, discard)
        hand.remove(card)
        discard.append(card[Card.valueIndex])
        return (hand, discard, card[Card.colorIndex])

    def card_discard(self, card):
        # Hand to Discard
        hand = self.player()[Player.handIndex]
        discard = self.discard[card[Card.colorIndex]]
        hand, discard, discardColor = Model.play_option_discard(hand, card, discard)
        self.player()[Player.handIndex] = hand
        self.discard[card[Card.colorIndex]] = discard
        self.discardLastColor = discardColor
        #self.player()[Player.handIndex].remove(card)
        #self.discard[card[Card.colorIndex]].append(card[Card.valueIndex])
        #self.discardLastColor = card[Card.colorIndex]

    @staticmethod
    def play_option_play(hand, card, boardState):
        hand.remove(card)
        color, value = card
        boardState |= 1 << (value + Config.cardsInColorCount * color)
        return (hand, value, boardState)

    def card_play(self, card):
        # Hand to Board
        p = self.player()
        color, _ = card
        hand, board, boardState = Model.play_option_play(
            p[Player.handIndex],
            card,
            p[Player.boardStateIndex])
        p[Player.handIndex] = hand
        p[Player.boardIndex][color] = board
        p[Player.boardStateIndex] = boardState

        #color, value = card
        #p[Player.handIndex].remove(card)
        #p[Player.boardIndex][color] = value
        #p[Player.boardStateIndex] |= 1 << (value + Config.cardsInColorCount * color)
        self.discardLastColor = None

    @staticmethod
    def pull_option_pull(hand, discard, color):
        hand.append((color, discard.pop()))
        return (hand, discard)

    def card_pull(self, color):
        # Discard to Hand
        p = self.player()
        hand, discard = Model.pull_option_pull(
            p[Player.handIndex],
            self.discard[color],
            color
        )
        p[Player.handIndex] = hand
        self.discard[color] = discard
        #p[Player.handIndex].append((color, self.discard[color].pop()))
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
            #print("GAME OVER")
            #print(self)
            p1Score = Player.board_score(self.players[0][Player.boardStateIndex])
            p2Score = Player.board_score(self.players[1][Player.boardStateIndex])
            if p1Score > p2Score:
                self.winner = 1
                #print('Player 1 Wins: ', p1Score, p2Score)
            elif p2Score > p1Score:
                self.winner = -1
                #print('Player 2 Wins: ', p1Score, p2Score)
            else:
                self.winner = 0
                #print('Tie: ', p1Score, p2Score)

    def play_random_turn(self):
        self.turnPly += 1
        p = self.player()
        # 1. PLAY: From hand to (board or discard)
        o = Player.play_options(p[Player.handIndex], p[Player.boardIndex])
        a = random.randrange(0, Config.cardsInHandCount + len(o))
        if a < Config.cardsInHandCount:
            color, value = p[Player.handIndex].pop(a)
            self.discard[color].append(value)
            self.discardLastColor = color
            #self.card_discard(p[Player.handIndex][a])
        else:
            card = o[a-Config.cardsInHandCount]
            p[Player.handIndex].remove(card)
            color, value = card
            p[Player.boardIndex][color] = value
            p[Player.boardStateIndex] |= 1 << (value + 12 * color)
            #self.card_play(o[a-Config.cardsInHandCount])

        # 2. PULL: From (deck or discard) to hand
        o = Player.pull_options(self.discard, self.discardLastColor)
        a = random.randrange(0, 1 + len(o))
        if o and a:
            color = o[a-1]
            card = (color, self.discard[color].pop())
            p[Player.handIndex].append(card)
            #self.card_pull(o[a-1])
        else:
            self.deck, card = Deck.cardChoice(self.deck, self.cardsInDeckCount)
            p[Player.handIndex].append(card)
            self.cardsInDeckCount -= 1
            #self.card_deal()

        if self.turnPly > 400:
            self.winner = -1
            return

        # 3. Winner?
        if not self.cardsInDeckCount:
            p1Score = Player.board_score(self.players[0][Player.boardStateIndex])
            p2Score = Player.board_score(self.players[1][Player.boardStateIndex])
            if p1Score > p2Score:
                self.winner = 1
            elif p2Score > p1Score:
                self.winner = -1
            else:
                self.winner = 0
            return

        self.playerActiveIndex = 0 if self.playerActiveIndex else 1

    def state(self):
        return [
            self.deck,
            self.playerActiveIndex,
            self.players[0],
            self.discard,
            self.players[1],
            self.discardLastColor,
            self.cardsInDeckCount
        ]