"""Terminal view for model display"""
import os
import time

from colorama import init, Fore, Back, Style
init()
from termcolor import cprint, colored
from pyfiglet import figlet_format

from view import viewinterface as v


class TerminalState(object):
    """describe mode of terminal view from intial load, menu, and game"""
    load = 0 #Initial load
    menu = 1 #Menu Screen
    game = 2 #Play Game

class TerminalView(v.ViewInterface):

    def init(self, game_manager):
        """Keep model and start new game"""
        self.game_manager = game_manager
        self.view_state = TerminalState.load
        self.menu_key = 0 #Default key
        self.menu_options = [k for k in self.game_manager.games.keys()]
        self.menu_options.extend([
            "Quit"
        ])

    def game_new(self):
        print('new game started!')
        self.view_state = TerminalState.game

    def handle_events(self):
        if self.view_state == TerminalState.menu:
            answer = input("\n\rType menu number or use [U]p/[D]own\n\r").upper()
            if answer.isdigit():
                self.menu_key = max(min(len(self.menu_options), int(answer))-1, 0)
            elif answer == "U":
                if self.menu_key > 0:
                    self.menu_key -= 1
            elif answer == "D":
                if self.menu_key < len(self.menu_options) - 1:
                    self.menu_key += 1

            if not answer:
                if self.menu_key == len(self.menu_options)-1:
                    raise SystemExit
                else:
                    self.game_manager.game_select('Tic Tac Toe')
                    print(self.game_manager.game.name)
                    self.game_manager.game_play()
                    input()

    def update(self):
        """no internal state to update for terminal view"""
        pass

    def display_clear(self):
        """Utility for cross platform terminal clear"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_display(self):
        """basic menu"""
        self.display_clear()
        link = 'https://github.com/Jagermeister'
        cprint(
            figlet_format('Expeditions!', font='big') + 
            ' '*(56-len(link)) + link
            , 'yellow', 'on_blue', attrs=['bold'])
        print("Main Menu\n\r")
        for i, menu in enumerate(self.menu_options):
            selected = i == self.menu_key
            f = "yellow"
            b = "blue"
            print((">   " if selected else "    ") + colored("{}. {}".format(
                i+1, menu), b if selected else f, 'on_' + (f if selected else b)))

    def display(self):
        if self.view_state == TerminalState.load:
            self.view_state = TerminalState.menu
        if self.view_state == TerminalState.menu:
            self.menu_display()

    def quit(self):
        pass