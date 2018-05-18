import random
from card import Card
from config import Config
Config = Config()

# Any container of cards
class Deck:
    @staticmethod
    def create(cardCount):
        return 2**cardCount - 1
    
    @staticmethod
    def cardPeek(container, cardCount):
        unsetIndex = random.randrange(cardCount)
        while unsetIndex:
            container &= container - 1
            unsetIndex -= 1
        return len(bin(container)) - len(bin(container).rstrip('0'))

    @staticmethod
    def cardChoice(containerFrom, cardCount):
        card = Deck.cardPeek(containerFrom, cardCount)
        return Card.remove(containerFrom, card), (Card.color(card), Card.value(card))

    @staticmethod
    def color(container, colorIndex):
        colorCards = Config.cardsInColorCount
        return (container >> (colorIndex * colorCards)) & ((1 << colorCards) - 1)