import math
import random

# MCTS scalar.
# Larger scalar will increase exploitation, smaller will increase exploration.
SCALAR = 1 / math.sqrt(2.0)

class Node():
    def __init__(self, state, parent=None, move=None):
        self.visits = 0
        # Each time the node is exploited
        self.reward = 0
        # Sum of all simulated results
        self.state = state#copy.deepcopy(state)
        # IS DEEP COPY REQUIRED??
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
                      math.sqrt(2 * math.log(self.visits) / c.visits))[-1]

    @staticmethod
    def child_score(parent, child):
        return child.reward / child.visits + math.sqrt(2 * math.log(parent.visits) / child.visits)

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

        print(self.reward, self.visits)
        children = sorted(self.children, 
            key=lambda c: c.visits, reverse=True)[:4]
        print('#\tReward\tVisits\tExploit\tExplore\tNext\tMove')
        for i, c in enumerate(children):
            print('C{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                i, c.reward, c.visits,
                round(c.reward / c.visits, 2),
                round(math.sqrt(
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
                        round(math.sqrt(
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


def UTCSearch(root, iterations):
    for i in range(1, iterations):
        if i % 1000:
            print('simulation:', i)


def EXPAND(node):
    node.child_add()
    return node.children[-1]


def BESTCHILD(node, scalar):
    bestScore = 0.0
    bestChildren = []
    for c in node.children:
        exploit = c.reward / c.visits
        explore = math.sqrt(2.0 * math.log(node.visits) / float(c.visits))
        score = exploit + scalar * explore
        if score == bestScore:
            bestChildren.append(c)
        elif score > bestScore:
            bestScore = score
            bestChildren = [c]
    return random.choice(bestChildren)


def TREEPOLICY(node):
    # Explore / Exploit determination
    while not node.terminal():
        if node.children and (node.is_fully_expanded() or random.uniform(0, 1) < 0.5):
            node = BESTCHILD(node, SCALAR)
        else:
            return EXPAND(node)
    return node


def DEFAULTPOLICY(state):
    # Simulate to terminal point, returning reward
    while not state.is_terminal:
        state = state.state_step_random()
    return state.reward


def BACKUP(node, reward):
    while node:
        node.update(reward)
        node = node.parent
