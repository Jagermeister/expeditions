""" View phase for selecting and configuring a game """

from termcolor import cprint
from pyfiglet import figlet_format

from src.view.terminal.listoptiondisplay import ListOptionsDisplay
from src.view.terminal.utilities import display_clear
from src.view.terminal.viewphase.viewphase import ViewPhase


def display_header():
    """ Developer banner display """
    display_clear()
    link = 'https://github.com/Jagermeister'
    cprint(
        figlet_format('Expeditions!', font='big') +
        ' '*(56-len(link)) + link
        , 'yellow', 'on_blue', attrs=['bold'])

class SetupPhase(ViewPhase):
    """ Game configuration phase """

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.title = 'Select Game'
        self.options_set(
            self.game_manager.games_available(),
            self.on_game_selected)

    def options_set(self, options=None, on_selected=None):
        """ Setup available game options and callback
        Args:
            options: [str] - Option names
            on_selected: callable - Callback function onSelected
        """
        self.setup_options = options if options else []
        self.list_displayer = ListOptionsDisplay(self.setup_options, on_selected)

    def options_clear(self):
        """ Remove all options """
        self.options_set()

    def on_game_selected(self, game_name):
        """ Callback when game is selected """
        self.game_manager.game_select_by_name(game_name)
        self.options_set_players()

    def options_set_players(self):
        """ Updates options for selecting players """
        player_count = self.game_manager.player_count() + 1
        self.title = 'Setting Up >>> {} <<<\r\nSelect Player {}'.format(
            self.game_manager.game.name,
            player_count)
        self.options_set(
            self.game_manager.players_available(),
            self.on_player_selected)

    def on_player_selected(self, player_name):
        """ Callback on player selection """
        self.game_manager.player_add_by_name(player_name)
        if self.game_manager.is_player_needed:
            self.options_set_players()
        else:
            self.options_clear()

    @property
    def is_complete(self):
        """ Is this view phase over? """
        return self.game_manager.game and not self.game_manager.is_player_needed

    def handle_events(self):
        """ Issue and process user events """
        self.list_displayer.handle_events()

    def display(self):
        """ Visual display of state """
        display_header()
        print(self.title)
        self.list_displayer.display()
