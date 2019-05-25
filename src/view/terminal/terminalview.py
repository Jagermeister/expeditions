"""Terminal view for model display"""

from enum import Enum

from src.view import viewinterface as v
from src.view.terminal.gamemanagerview import GameManagerView


class TerminalState(Enum):
    """describe mode of terminal view from intial load, menu, and game"""
    LOAD = 0        # Initial load
    MENU = 1        # Menu Screen
    GAME_PLAY = 2   # Play Game
    GAME_REVIEW = 3 # Review Game State
    GAME_OVER = 4        # Game Over

class TerminalView(v.ViewInterface):
    """ Concrete command line display """

    def init(self):
        """ Keep model and start new game """
        self.game_manager = GameManagerView()
        #self.view_state = TerminalState.load

    def handle_events(self):
        """ Process actions and interact with model """
        self.game_manager.handle_events()

    def update(self):
        """ Internal state of view objects """
        self.game_manager.update()

    def display(self):
        """ Visual display of state """
        self.game_manager.display()

    def quit(self):
        """ Unload any assets before exit """
