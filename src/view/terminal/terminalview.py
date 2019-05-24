"""Terminal view for model display"""
import os
import time

from colorama import init, Fore, Back, Style
init()
from termcolor import cprint, colored
from pyfiglet import figlet_format

from src.view import viewinterface as v
from src.view.terminal.gamemanagerview import GameManagerView

class TerminalState(object):
    """describe mode of terminal view from intial load, menu, and game"""
    load = 0 #Initial load
    menu = 1 #Menu Screen
    game_play = 2 #Play Game
    game_review = 3
    over = 4 #Game Over

class TerminalView(v.ViewInterface):

    def init(self):
        """Keep model and start new game"""
        self.game_manager = GameManagerView()
        #self.view_state = TerminalState.load

    def handle_events(self):
        self.game_manager.handle_events()
        #if self.view_state == TerminalState.menu:
        #    self.game_manager.handle_events()
        #elif self.view_state == TerminalState.game_review:
        #    self.game_manager.handle_events()

    def update(self):
        """no internal state to update for terminal view"""
        self.game_manager.update()

    def display(self):
        self.game_manager.display()

    def quit(self):
        pass