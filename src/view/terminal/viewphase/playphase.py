""" Playing the selected game display """

from src.view.terminal.viewphase.viewphase import ViewPhase

class PlayPhase(ViewPhase):
    """ Playing the selected game display """

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.game_manager.game.setup()

    @property
    def is_complete(self):
        """ Is this view phase over? """
        return self.game_manager.is_terminal

    def update(self):
        """ Internal state of view objects """
        self.game_manager.play_turn()
