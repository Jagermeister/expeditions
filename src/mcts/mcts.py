""" Monte Carlo Tree Search
    Main min-max search algorithm for trees named
    Upper Confidence Bounds for Trees (UCT)
"""

from math import sqrt, log
from random import randrange

from colorama import init, Fore, Back, Style

from src.model.config import Config

# Initialize colorama and configuration
init()
CONFIG = Config()

# Monte Carlo Tree Search
SCALAR = 1 / sqrt(2.0)
#Larger values will increase exploitation, smaller will increase exploration

class Node():
    """ MCTS Node representing a current state """

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
                      SCALAR * sqrt(2 * log(self.visits) / c.visits))[-1]

    @staticmethod
    def child_score(parent, child):
        return Node.exploit_score(child) + Node.explore_score(parent, child)

    @staticmethod
    def exploit_score(child):
        return child.reward / child.visits

    @staticmethod
    def explore_score(parent, child):
        return SCALAR * sqrt(2 * log(parent.visits) / child.visits)

    @staticmethod
    def move_display(move):
        play, (card, pull) = move
        color, value = card
        _, short_name, color_back, color_fore = CONFIG.colors[color]
        value_display = 'X' if value < CONFIG.betCount else str(value + 2 - CONFIG.betCount)
        if pull == 'd':
            pull_display = 'pull from deck'
        else:
            name, _, pull_color_back, pull_color_fore = CONFIG.colors[pull]
            pull_display = f'pull discard {pull_color_back}{pull_color_fore}{name} ({pull})'
        return color_back + color_fore + (' ' if len(value_display) else '') + value_display + short_name + ' ' + \
             Back.BLACK + Fore.WHITE + play + ',\t' + pull_display

    def children_display(self, children=None, depth=2, maxDepth=2, top=4):
        if not depth:
            return

        if children is None:
            children = self.children

        depth_current = maxDepth - depth
        children = sorted(children, key=lambda c: c.visits, reverse=True)[:top]
        print('{}\tReward\tVisits\tExploit\tExplore\tNext\tPlay Move\tPull Move'.format(
            '#' if not depth_current else '>VV'
        ))
        for i, child in enumerate(children):
            exploit, explore = Node.exploit_score(child), Node.explore_score(self, child)
            print('{}{}{}\t{}\t{}\t{}\t{}\t{}\t{}{}'.format(
                '>'*depth_current,
                'ABCDEF'[depth_current],
                i, child.reward, child.visits,
                round(exploit, 2),
                round(explore, 2),
                round(exploit + explore, 2),
                Node.move_display(child.move),
                Style.RESET_ALL))
            if i == 0 and children[i].children:
                self.children_display(children[i].children, depth - 1)

    def reward_update(self, reward):
        self.reward += reward
        self.visits += 1

    def moves_generate(self):
        """ From state, determine possible moves """
        pass

    def move_untried(self, index):
        """ Select untried move by index """
        pass

    def advance_by_move(self, move):
        """ Return new state """
        pass


def UCT(root_node, iterations):
    for i in range(1, iterations+1):
        if i % 5000 == 0:
            print(f'simulation: {i}')
        node = root_node

        # Select candidate
        while not node.untried_move_count and node.children:
            node = node.child_best()

        # Expand
        if node.untried_move_count:
            move = node.move_untried(randrange(0, node.untried_move_count))
            state = node.advance_by_move(move)
            node.child_add(state, move)
            node = node.children[-1]

        # Rollout
        if not node.is_terminal:
            node.advance_to_terminal()

        # Backpropagate
        reward = node.terminal_reward
        while node:
            node.reward_update(reward)
            node = node.parent

    return sorted(root_node.children, key=lambda c: c.visits)[-1]
