from colorama import Back, Fore

class ConfigDevelopment:
    colorCount = 3
    #How many different suites/colors are there?
    valueCount = 6
    #How many distinct, ascending value options
    #per color are there?
    betCount = 2
    #How many HandShake/Bet/Score multiplier cards
    #per color are there?
    cardsInHandCount = 6
    #How many cards in a player's hand?
    expeditionCost = 12
    #Point cost to start an expedition
    turnsUntilForcedLoss = 200
    #After this many turns, the first player loses

    colors = {
        0: ('Red', 'r', Back.BLACK, Fore.RED),
        1: ('Yellow', 'y', Back.YELLOW, Fore.BLACK),
        2: ('Blue', 'b', Back.BLACK, Back.BLUE)
    }

    @property
    def cardsInColorCount(self):
        return self.valueCount + self.betCount

    @property
    def cardsInDeckCount(self):
        return self.colorCount * self.cardsInColorCount