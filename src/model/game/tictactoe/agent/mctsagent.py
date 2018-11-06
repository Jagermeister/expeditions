from ...agent.mctsagent import MCTSAgent
from .mctsnode import TTTNode

class TTTMCTSAgent(MCTSAgent):
    iterations = 750
    is_debug = False

    def state_to_node(self):
        return TTTNode(self.model.state)