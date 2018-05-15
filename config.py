
class Config:
    colorCount = 5
    #How many different suites/colors are there?
    valueCount = 9
    #How many distinct, ascending value options
    #per color are there?
    betCount = 3
    #How many HandShake/Bet/Score multiplier cards
    #per color are there?
    cardsInHandCount = 8
    #How many cards in a player's hand?

    @property
    def cardsInColorCount(self):
        return self.valueCount + self.betCount

    @property
    def cardsInDeckCount(self):
        return self.colorCount * self.cardsInColorCount