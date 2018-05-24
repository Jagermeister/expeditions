from ..game import Game

class Agent:

    def __init__(self, name, model):
        assert isinstance(model, Game)
        self.name = name
        self.model = model

    def update(self, move_opponent):
        pass

    def move_from_state(self):
        pass
