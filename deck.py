import random
from card import Card

# Any container of cards
class Deck:
    @staticmethod
    def create(cardCount):
        return 2**cardCount - 1
    
    @staticmethod
    def cardPeek(container, cardCount):
        unsetIndex = random.randrange(cardCount)
        cs = container
        while unsetIndex:
            cs &= cs - 1
            unsetIndex -= 1
        index = len(bin(container)) - len(bin(cs).rstrip('0'))
        return index

    @staticmethod
    def cardChoice(containerFrom, cardCount):
        card = Deck.cardPeek(containerFrom, cardCount)
        return Card.remove(containerFrom, card), (Card.color(card), Card.value(card))

    @staticmethod
    def color(container, colorIndex):
        # HARDCODED 12 is number of cards per color
        return (container >> (colorIndex * 12)) & ((1 << 12) - 1)