"""Terminal view for model display"""
from view import viewinterface as v

class TerminalView(v.ViewInterface):

    def init(self, model):
        """Keep model and start new game"""
        self.model = model

    def handle_events(self):
        input('what?')
        pass

    def update(self):
        """no internal state to update for terminal view"""
        pass

    def display(self):
        print('hello')

    def quit(self):
        pass