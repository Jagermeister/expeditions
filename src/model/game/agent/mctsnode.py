from math import sqrt, log


# Monte Carlo Tree Search
SCALAR = 1 / sqrt(2.0)
#Larger values will increase exploitation, smaller will increase exploration

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
        self.terminal_reward = None
        self.moves_generate()
        self.reward_stats_win_lose_tie = [0, 0, 0]

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

    def children_display(self, children=None, depth=2, maxDepth=2, top=4):
        if not depth:
            return

        if children is None:
            children = self.children

        d = maxDepth-depth
        children = sorted(children, key=lambda c: c.visits, reverse=True)[:top]
        print('{}\tReward\tWin/Lose/Tie\tVisits\tExploit\tExplore\tNext\tPlay Move\tPull Move'.format(
            '#' if not d else '>VV'
        ))
        for i, c in enumerate(children):
            exploit, explore = Node.exploit_score(c), Node.explore_score(self, c)
            print('{}{}{}\t{}\t{:03d}/ {:03d}/{:03d}\t{}\t{}\t{}\t{}\t{}'.format(
                '>'*d,
                'ABCDEF'[d],
                i, c.reward,
                c.reward_stats_win_lose_tie[0],
                c.reward_stats_win_lose_tie[1],
                c.reward_stats_win_lose_tie[2],
                c.visits,
                round(exploit, 2),
                round(explore, 2),
                round(exploit + explore, 2),
                c.move))
            if i == 0 and children[i].children:
                self.children_display(children[i].children, depth-1)

    def reward_update(self, reward):
        self.reward += reward
        self.visits += 1
        if reward == 0.5:
            self.reward_stats_win_lose_tie[2] += 1
        elif reward:
            self.reward_stats_win_lose_tie[0] += 1
        else:
            self.reward_stats_win_lose_tie[1] += 1

    def moves_generate(self):
        # From state, determine possible moves
        pass

    def move_untried(self, index):
        # Select untried move by index
        pass

    def advance_by_move(self, move):
        # Return new state
        pass

    def advance_to_terminal(self):
        pass