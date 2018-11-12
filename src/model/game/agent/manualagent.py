from .agent import Agent

class ManualAgent(Agent):
    name = 'Manual'

    def move_from_state(self):
        self.model.state_display()
        return int(input())