from ...agent.agent import Agent

class RuleFirstAvailableAgent(Agent):
    name = 'Rule: First available'

    def move_from_state(self):
        return self.model.moves_available()[0]