from ...agent.agent import Agent

class ManualAgent(Agent):
    name = 'Manual'

    def move_from_state(self):
        print(self.model.state)
        return int(input())