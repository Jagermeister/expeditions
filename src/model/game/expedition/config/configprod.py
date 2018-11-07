from .configuration import Configuration
from colorama import Back, Fore

class Production(Configuration):
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
    expeditionCost = 20
    #Point cost to start an expedition
    turnsUntilForcedLoss = 400
    #After this many turns, the first player loses

    colors = {
        0: ('Red', 'r', Back.BLACK, Fore.RED),
        1: ('Yellow', 'y', Back.YELLOW, Fore.BLACK),
        2: ('Blue', 'b', Back.BLACK, Back.BLUE),
        3: ('Green', 'g', Back.BLACK, Fore.GREEN),
        4: ('White', 'w', Back.BLACK, Fore.WHITE)
    }