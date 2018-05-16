import math
import random

# MCTS scalar.
# Larger scalar will increase exploitation, smaller will increase exploration.
SCALAR = 0.5#1 / math.sqrt(2.0)

class Node():
    def __init__(self, state, parent=None, move=None):
        self.visits = 0
        # Each time the node is exploited
        self.reward = 0
        # Sum of all simulated results
        self.state = state
        # Model representation
        self.parent = parent
        self.children = []
        self.untried_move_count = 0
        self.move = move
        self.is_terminal = False
        self.moves_generate()

    def child_add(self, state, move):
        self.children.append(Node(state, self, move))

    def child_best(self):
        return sorted(self.children, key=lambda c:
                      c.reward / c.visits +
                      SCALAR * math.sqrt(2 * math.log(self.visits) / c.visits))[-1]

    @staticmethod
    def child_score(parent, child):
        return child.reward / child.visits + SCALAR * math.sqrt(2 * math.log(parent.visits) / child.visits)

    def children_display(self):
        cards = sorted(self.state[2][0], key=lambda c: (c[0], c[1]))
        colors = {
            0: 'red',
            1: 'yellow',
            2: 'blue',
            3: 'green',
            4: 'white'
        }
        #print('Colors: ', colors)
        #print('Cards: ', end='')
        #for i, c in cards:
        #    print(('X' if c < 3 else str(c-1)) +' '+colors[i]+', ', end='')
        #print()

        print(self.visits, self.reward)
        children = sorted(self.children, 
            key=lambda c: c.visits, reverse=True)[:4]
        print('#\tReward\tVisits\tExploit\tExplore\tNext\tMove')
        for i, c in enumerate(children):
            print('C{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                i, c.reward, c.visits,
                round(c.reward / c.visits, 2),
                round(SCALAR * math.sqrt(
                    2 * math.log(self.visits) / c.visits), 2),
                round(Node.child_score(self, c), 2),
                c.move))
            if i == 0 and children[i].children:
                subchilds = sorted(children[i].children, 
                    key=lambda c: c.visits, reverse=True)[:4]
                for ii, cc in enumerate(subchilds):
                    print(' >\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                        cc.reward, cc.visits,
                        round(cc.reward / cc.visits, 2),
                        round(SCALAR * math.sqrt(
                            2 * math.log(c.visits) / cc.visits), 2),
                        round(Node.child_score(c, cc), 2),
                        cc.move))



    def reward_update(self, reward):
        self.reward += reward
        self.visits += 1

    def moves_generate(self):
        # From state, determine possible moves
        pass

    def move_untried(self, index):
        # Select untried move by index
        pass

    def advance_by_move(self, move):
        pass

import copy
def UCT(root_node, iterations):
    for i in range(1, iterations+1): 
        if i % 5000 == 0:
            print('simulation:', i)
        # Init
        #print('!! ROOT', root_node.state)
        #root_node.children_display()
        node = root_node

        # Select candidate
        while not node.untried_move_count and node.children:
            node = node.child_best()

        # Expand
        if node.untried_move_count:
            move = node.move_untried(random.randrange(0, node.untried_move_count))
            #print('move', move)
            #print('before', node.state)
            state = node.advance_by_move(move)
            #print('after', state)
            node.child_add(state, move)
            #node.children_display()
            node = node.children[-1]

        #Rollout
        if not node.is_terminal:
            node.advance_to_terminal()

        #Backpropagate
        reward = node.terminal_reward
        while node:
            node.reward_update(reward)
            node = node.parent
        
    #root_node.children_display()
    return sorted(root_node.children, key=lambda c: c.visits)[-1]