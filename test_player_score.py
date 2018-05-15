import unittest
from player import Player
from card import Card

class TestPlayerScore(unittest.TestCase):

    def validateSet(self, testSet):
        for i, t in enumerate(testSet):
            self.subTest('{} {}'.format(i, t))
            self.subTest(i=i)
            board, score = t
            self.validateCase(board, score)

    def validateCase(self, board, score):
        s = Player.board_score(board)
        self.assertEqual(s, score)

    def test_bets(self):
        # First 3 bits represent three HandShake cards.
        cost = -20
        testCases = [
            [0, 0],
            [1, cost*2],
            [2, cost*2],
            [4, cost*2],
            [3, cost*3],
            [6, cost*3],
            [5, cost*3],
            [7, cost*4]
        ]
        self.validateSet(testCases)

    def test_no_bets(self):
        cost = -20
        testCases = [
            [0b1000, cost + 2],
            [0b10000, cost + 3],
            [0b100000, cost + 4],
            [0b1000000, cost + 5],
            [0b10000000, cost + 6],
            [0b100000000, cost + 7],
            [0b1000000000, cost + 8],
            [0b10000000000, cost + 9],
            [0b100000000000, cost + 10],
            [0b100001011000, 0],
            [0b111000, cost + 2 + 3 + 4]
        ]
        self.validateSet(testCases)

    def test_bets_with_cards(self):
        cost = -20
        testCases = [
            [0b100001000000, cost + 10 + 5],
            [0b100001000001, (cost + 10 + 5) * 2],
            [0b100001000010, (cost + 10 + 5) * 2],
            [0b100001000100, (cost + 10 + 5) * 2],
            [0b100001000101, (cost + 10 + 5) * 3]
        ]
        self.validateSet(testCases)

    def test_multiple_colors(self):
        cost = -20
        testCases = [
            [0b000111000000 << 12 | 0b100001000000, 
                cost + 7 + 6 + 5 + cost + 10 + 5],
        ]
        self.validateSet(testCases)

if __name__ == '__main__':
    unittest.main()