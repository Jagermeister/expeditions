from random import randrange

from .agent import Agent
from .mctsnode import Node

class MCTSAgent(Agent):
    name = "Monte Carlo Tree Search"
    iterations = None
    is_debug = False

    def __init__(self, model):
        self.model = model
        self.root = None

    def update(self, move_opponent):
        self.model.move_play(move_opponent)

    def move_from_state(self):
        node = self.simulations_run()
        return node.move

    def state_to_node(self):
        pass

    def simulations_run(self):
        root_node = self.state_to_node()
        assert(isinstance(root_node, Node))
        for i in range(1, self.iterations+1):
            if i % 5000 == 0: print('simulation:', i)
            node = root_node

            # Select candidate
            while not node.untried_move_count and node.children:
                node = node.child_best()

            #if self.is_debug:
            #    print(root_node.moves, node.move)
            #    print(root_node.children_display())

            # Expand
            if node.untried_move_count:
                [move, attempts] = node.move_untried(randrange(0, node.untried_move_count))
                state = node.advance_by_move(move)
                if attempts == 1:
                    node.child_add(state, move)
                    node = node.children[-1]
                else:
                    node = [n for n in node.children if n.move == move][0]

            # Rollout
            #if not node.is_terminal:
            node.advance_to_terminal()

            # Backpropagate
            reward = node.terminal_reward
            while node:
                node.reward_update(reward)
                reward = abs(reward - 1)
                node = node.parent

        if self.is_debug:
            print(self.model.state_display(self.model.state))
            root_node.children_display(top=100)
            input('children display')

        return sorted(root_node.children, key=lambda c: c.visits)[-1]