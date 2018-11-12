import os

from colorama import init, Fore, Back, Style
init()
from termcolor import cprint
from pyfiglet import figlet_format

from model.gamemanager import GamesManager
from .listoptiondisplay import ListOptionsDisplay

def display_clear():
    """Utility for cross platform terminal clear"""
    os.system('cls' if os.name == 'nt' else 'clear')

class SetupPhase():

    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.title = 'Select Game'
        self.options_set(
            self.game_manager.games_available(),
            self.on_game_selected)

    def options_set(self, options=[], on_selected=None):
        self.setup_options = options
        self.list_displayer = ListOptionsDisplay(self.setup_options, on_selected)

    def options_clear(self):
        self.options_set()

    def on_game_selected(self, game_name):
        self.game_manager.game_select_by_name(game_name)
        self.options_set_players()

    def options_set_players(self):
        player_count = self.game_manager.player_count() + 1
        self.title = 'Setting Up >>> {} <<<\r\nSelect Player {}'.format(
                self.game_manager.game.name,
                player_count)
        self.options_set(
            self.game_manager.players_available(),
            self.on_player_selected)
    
    def on_player_selected(self, player_name):
        self.game_manager.player_add_by_name(player_name)
        if self.game_manager.is_player_needed:
            self.options_set_players()
        else:
            self.options_clear()

    @property
    def is_complete(self):
        return self.game_manager.game and not self.game_manager.is_player_needed

    def handle_events(self):
        self.list_displayer.handle_events()

    def update(self):
        pass

    def display(self):
        self.display_header()
        print(self.title)
        self.list_displayer.display()

    def display_header(self):
        display_clear()
        link = 'https://github.com/Jagermeister'
        cprint(
            figlet_format('Expeditions!', font='big') + 
            ' '*(56-len(link)) + link
            , 'yellow', 'on_blue', attrs=['bold'])

class PlayPhase():
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.game_manager.game.setup()

    @property
    def is_complete(self):
        return self.game_manager.is_terminal

    def handle_events(self):
        pass

    def update(self):
        self.game_manager.play_turn()

    def display(self):
        pass

class ExaminePhase():
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.examine_options = ["Previous State", "Next State"]
        self.list_displayer = ListOptionsDisplay(self.examine_options, self.on_state_selected)
        self.state_index = len(self.game_manager.game_states) - 1
        self.state = self.game_manager.game_states[self.state_index]

    def on_state_selected(self, value):
        if value == "Previous State" and self.state_index > 0:
            self.state_index -= 1
        elif value == "Next State" and self.state_index < len(self.game_manager.game_states) - 1:
            self.state_index += 1

        self.state = self.game_manager.game_states[self.state_index]

    def handle_events(self):
        self.list_displayer.handle_events()

    def update(self):
        pass

    def display(self):
        display_clear()
        print('Examine Mode')
        for i, p in enumerate(self.game_manager.game.players):
            print('Player {}: {}'.format(i+1, p.name))
        self.game_manager.game.state_display(self.state)
        print('\n\r')
        self.list_displayer.display()


class GameManagerViewState(object):
    init = 0
    setup = 1
    play = 2
    examine = 3

class GameManagerView():

    def __init__(self):
        self.game_manager = GamesManager()
        self.state = GameManagerViewState.init
        self.phase = None
        
        self.games_to_play = 10
        self.games = 0
        self.game_score_by_player = {}

    def handle_events(self):
        if self.phase:
            self.phase.handle_events()

    def update(self):
        if self.state == GameManagerViewState.init:
            self.state = GameManagerViewState.setup
            self.phase = SetupPhase(self.game_manager)
        elif self.state == GameManagerViewState.setup and self.phase.is_complete:
            self.state = GameManagerViewState.play
            self.phase = PlayPhase(self.game_manager)
            for i in range(self.game_manager.game.player_count):
                self.game_score_by_player[i] = 0
            print('Game {} - Play!'.format(self.games+1))

        elif self.state == GameManagerViewState.play and self.phase.is_complete:
            self.games += 1
            self.game_manager.game.state_display()

            r = self.game_manager.game.reward()
            if self.game_manager.game.player_count == 1:
                currPlayerIndex = 0
            else:
                currPlayerIndex = 0 if self.game_manager.game.turn_ply % self.game_manager.game.player_count else 1

            if r == 1:
                print('Winner: Player {}'.format(currPlayerIndex + 1))
                self.game_score_by_player[currPlayerIndex] += 1
            elif r == 0.5:
                print('Tied!')
                for key in self.game_score_by_player:
                    self.game_score_by_player[key] += 0.5
            else:
                print('Player 1 Lost')
                for key in self.game_score_by_player:
                    if key != currPlayerIndex:
                        self.game_score_by_player[key] += 1

            if self.games < self.games_to_play:
                self.phase = PlayPhase(self.game_manager)
                self.game_manager.game.reset()

            print('Game {} - Score By Players: {}\n\r'.format(
                self.games,
                ', '.join([str(self.game_score_by_player[key]) for key in self.game_score_by_player])
            ), flush=True)

            if self.games == self.games_to_play:
                input('Game Over')
                self.state = GameManagerViewState.examine
                self.phase = ExaminePhase(self.game_manager)

        self.phase.update()

    def display(self):
        self.phase.display()

    def play_turn(self):
        self.game_manager.play_turn()
