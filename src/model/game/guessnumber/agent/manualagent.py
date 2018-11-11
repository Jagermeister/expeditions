from ...agent.agent import Agent
from ..GuessGame import GuessGame

class ManualAgent(Agent):
    name = 'Manual'

    def move_from_state(self):
        GuessGame.state_display(self.model.state)
        return int(input())