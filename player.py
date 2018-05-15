from card import Card
from deck import Deck

class Player:
    handIndex = 0
    boardIndex = 1
    boardStateIndex = 2

    @staticmethod
    def create():#hand, board
        return [[], [-1]*5, 0b0]

    @staticmethod
    def play_options(hand, board):
        #return [c for c in hand if Player.is_playable(c, board)]
        return [c for c in hand if c[1] > board[c[0]] or (c[1] < 3 and board[c[0]] < 3)]
# 91459860 function calls (87508289 primitive calls) in 98.123 seconds
# 01548132  5.797   11.219  player.py:15(<listcomp>)
# 12385056  5.422           player.py:17(is_playable)

# 55235533 function calls (52037554 primitive calls) in 66.009 seconds
#   972977  4.034           player.py:16(<listcomp>)
    @staticmethod
    def is_playable(card, board):
        color, value = card
        pile = board[color]
        #print(card, board, value | pile, 0b10, value > pile or value | pile <= 0b10)
        return value > pile or (value < 3 and pile < 3)

    @staticmethod
    def pull_options(discard, discardCardColor=None):
        # each discard that has a card, that isnt discardCard
        if discardCardColor:
            return [i for i, x in enumerate(discard) if x and i != discardCardColor]
        else:
            return [i for i, x in enumerate(discard) if x]

    @staticmethod
    def board_score(board):
        score = 0
        while board:
            cards = board & ((1 << 12) - 1)
            if cards:
                score += Player.cards_score(cards)
            board >>= 12
        return score

    @staticmethod
    def cards_score(cards):
        score = -20
        betCount = 1
        i = 0
        while i < 3:
            betCount += cards & 0b1
            cards >>= 1
            i += 1

        i = 2
        while cards:
            score += i * (cards & 0b1)
            cards >>= 1
            i += 1
        return score * betCount