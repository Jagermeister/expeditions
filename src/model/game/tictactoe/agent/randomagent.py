from random import choice

from ...agent.agent import Agent

class RandomAgent(Agent):

    def __init__(self, model):
        super().__init__('Random', model)

    def move_from_state(self):
        return choice(self.model.moves_available())