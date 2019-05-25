""" Monte Carlo Tree Search
    Main min-max search algorithm for trees named
    Upper Confidence Bounds for Trees (UCT)
"""

from random import randrange


def mcts_utc(root_node, iterations):
    """ Monte Carlo Tree Search
    Args:
        root_node: Node - Starting item for searching
        iterations: int - Number of simulations to run
    """

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
