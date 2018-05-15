
bitTemplate = (1 << 60) - 1
# This should be a parameter (How many total
# cards? #60) but for clarity we keep it constant.
def bit_mask(index):
    return bitTemplate - (1 << index)

class Card:
    colorIndex = 0
    valueIndex = 1

    @staticmethod
    def add(container, cardIndex):
        return container | 1 << cardIndex

    @staticmethod
    def remove(container, cardIndex):
        return container & bit_mask(cardIndex)

    @staticmethod
    def color(index):
        return index // 12

    @staticmethod
    def value(index):
        return index % 12

    @staticmethod
    def to_index(card):
        color, value = card
        return 12 * color + value