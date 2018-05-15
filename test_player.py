import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    def test_isHandAttributeSet(self):
        self.assertEqual(Player.handIndex, 0)


if __name__ == '__main__':
    unittest.main()