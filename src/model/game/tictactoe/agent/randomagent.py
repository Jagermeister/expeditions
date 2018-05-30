from random import choice

from ...agent.agent import Agent

class RandomAgent(Agent):
    name = 'Random'

    def move_from_state(self):
        return choice(self.model.moves_available(self.model.state))