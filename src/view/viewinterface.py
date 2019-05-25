""" Template for views - these features should be fulfilled to interact with main.py """

class ViewInterface:
    """ Basic game loop functions """

    def init(self, model):
        """ Initialization, local use of model information """
        raise NotImplementedError

    def handle_events(self):
        """ Process actions and interact with model """
        raise NotImplementedError

    def update(self):
        """ Internal state of view objects """
        raise NotImplementedError

    def display(self):
        """ Visual display of state """
        raise NotImplementedError

    def quit(self):
        """ Unload any assets before exit """
        raise NotImplementedError
