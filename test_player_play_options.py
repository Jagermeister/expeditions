import unittest
from player import Player
from card import Card

class TestPlayerPlayOptions(unittest.TestCase):

    def validateSet(self, testSet):
        for i, t in enumerate(testSet):
            self.subTest('{} {}'.format(i, t))
            self.subTest(i=i)
            hand, board, options = t
            self.validateCase(hand, board, options)

    def validateCase(self, hand, board, options):
        os = Player.play_options(hand, board)
        self.assertEqual(len(options), len(os))
        for o in os:
            self.assertIn(o, options)

    def test_bets_play_without_order(self):
        # First 3 bits represent three HandShake cards.
        # They are considered the same value, for instance
        # 0b100 may be played first and then 0b010.
        testCases = [[
            [   (0, 0), (0, 1)
            ],  [2, -1, -1, -1, -1], [
                (0, 0), (0, 1)]
        ],[
            [   (0, 0), (0, 2)
            ],  [1, -1, -1, -1, -1], [
                (0, 0), (0, 2)]
        ],[
            [   (0, 0)
            ],  [2, -1, -1, -1, -1], [
                (0, 0)]
        ],[
            [   (0, 1)
            ],  [2, -1, -1, -1, -1], [
                (0, 1)]
        ]]
        self.validateSet(testCases)

    def test_ascending_plays_only(self):
        testCases = [[
            [   (0, 0), (0, 1), (0, 4)
            ],  [3, -1, -1, -1, -1], [
                (0, 4)]
        ],[
            [   (0, 0), (0, 2), (0, 9),
                (1, 6), (1, 8), (1, 1)
            ],  [8, 4, -1, -1, -1], [
                (0, 9), (1, 6), (1, 8)]
        ]]
        self.validateSet(testCases)

if __name__ == '__main__':
    unittest.main()