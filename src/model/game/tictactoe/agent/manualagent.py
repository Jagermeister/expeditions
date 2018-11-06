from ...agent.agent import Agent
from ..TTTGame import TTTGame

class ManualAgent(Agent):
    name = 'Manual'

    def move_from_state(self):
        print(TTTGame.state_display(self.model.state))
        return int(input())