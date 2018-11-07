class Configuration:
    colorCount = None
    #How many different suites/colors are there?
    valueCount = None
    #How many distinct, ascending value options
    #per color are there?
    betCount = None
    #How many HandShake/Bet/Score multiplier cards
    #per color are there?
    cardsInHandCount = None
    #How many cards in a player's hand?
    expeditionCost = None
    #Point cost to start an expedition
    turnsUntilForcedLoss = None
    #After this many turns, the first player loses

    colors = None
    #Dictionary of colorIndex to tuple
    # (Full Name, Abbreviation, Background Color, Foreground Color)

    def __str__(self):
        print('>>Game Settings: ', type(self).__name__)
        print('>>Colors:', self.colorCount,
            ' Values: 2 ->', self.valueCount+2-self.betCount,
            ' Bets:', self.betCount)
        print('>>CardsInHand:', self.cardsInHandCount,
            ' ColorCost:', self.expeditionCost)
        return ''

    @property
    def cardsInColorCount(self):
        return self.valueCount + self.betCount

    @property
    def cardsInDeckCount(self):
        return self.colorCount * self.cardsInColorCount