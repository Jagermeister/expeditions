""" Reviewing game state display """

from src.view.terminal.listoptiondisplay import ListOptionsDisplay
from src.view.terminal.utilities import display_clear
from src.view.terminal.viewphase.viewphase import ViewPhase


class ExaminePhase(ViewPhase):
    """ Reviewing game state display """

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.examine_options = ["Previous State", "Next State"]
        self.list_displayer = ListOptionsDisplay(self.examine_options, self.on_state_selected)
        self.state_index = len(self.game_manager.game_states) - 1
        self.state = self.game_manager.game_states[self.state_index]

    def on_state_selected(self, value):
        """ Callback on state option selection """
        if value == "Previous State" and self.state_index > 0:
            self.state_index -= 1
        elif value == "Next State" and self.state_index < len(self.game_manager.game_states) - 1:
            self.state_index += 1

        self.state = self.game_manager.game_states[self.state_index]

    def handle_events(self):
        """ Issue and process user events """
        self.list_displayer.handle_events()

    def display(self):
        """ Visual display of state """
        display_clear()
        print('Examine Mode')
        for i, player in enumerate(self.game_manager.game.players):
            print(f'Player {i+1}: {player.name}')

        self.game_manager.game.state_display(self.state)
        print('\n\r')
        self.list_displayer.display()
