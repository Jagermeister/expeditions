from ...agent.mctsagent import MCTSAgent
from .mctsnode import TTTNode

class TTTMCTSAgent(MCTSAgent):
    iterations = 25000
    is_debug = True

    def state_to_node(self):
        return TTTNode(self.model.state)