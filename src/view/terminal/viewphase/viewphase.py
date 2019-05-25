""" Abstract template for each game phase to implement for display """

class ViewPhase():
    """ Template to display information for a specific game phase """

    def __init__(self, game_manager):
        self.game_manager = game_manager

    @property
    def is_complete(self):
        """ Is this view phase over? """

    def handle_events(self):
        """ Issue and process user events """

    def update(self):
        """ Internal state of view phase """

    def display(self):
        """ Visual display of state """
