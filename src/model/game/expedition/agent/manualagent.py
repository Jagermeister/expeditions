from ...agent.agent import Agent
from ..player import Player

class ManualAgent(Agent):
    name = 'Manual'

    def __init__(self, model):
        super().__init__(model)
        self.player = Player.create()

    def move_from_state(self):
        print(self.model.state)
        return int(input())