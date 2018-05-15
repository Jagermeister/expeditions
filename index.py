from model import Model
from mcts_model import ExpeditionNode
from mcts import UCT

import time
from player import Player

def run_games(n):
    game = Model()
    now = time.clock()
    stats = {
        'turnPlys': 0,
        'p1': 0,
        'p2': 0,
        'tie': 0
    }

    for i in range(1, n):
        if i % 2500 == 0: print('#', i)
        game.setup()
        while game.cardsInDeckCount:
            game.play_random_turn()
        stats['turnPlys'] += game.turnPly
        if game.winner == 1:
            stats['p1'] += 1
        elif game.winner == -1:
            stats['p2'] += 1
        else:
            stats['tie'] += 1

    print(n, stats)
    print(time.clock() - now)

def record_move_stats(stats, move):
    action, (play, pull) = move
    if action == 'play':
        stats['play_card'] += 1
    else: 
        stats['play_discard'] += 1
    
    if pull == 'd':
        stats['pull_card'] += 1
    else:
        stats['pull_discard'] += 1

def run_mcts(n, modelState=None):
    model = None
    if modelState:
        model = Model.make_from_state(modelState, False)
    else:
        model = Model()
        model.setup()
    
    now = time.clock()
    move_stats = {
        'play_card': 0,
        'play_discard': 0,
        'pull_card': 0,
        'pull_discard': 0
    }
    while model.cardsInDeckCount:
        root = ExpeditionNode(model.state())
        node = UCT(root, n)
        print(node.move, model)
        node.parent.children_display()
        model.play_move(node.move)
        record_move_stats(move_stats, node.move)
        if model.cardsInDeckCount:
            model.play_random_turn()
        print(int(model.turnPly/2), model, flush=True)
        input()

    print(model.winner,
        Player.board_score(model.players[0][Player.boardStateIndex]),
        Player.board_score(model.players[1][Player.boardStateIndex])
    )
    print(move_stats)
    print(time.clock() - now)

def profile_mcts(n):
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    run_mcts(n)
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

# 5000 games in 14s w   1849770867 ply: 'p1': 2436, 'p2': 2499, 'tie': 65
test = [
    792280796199869815,
    0,
    [[(4, 0), (0, 9), (3, 10), (3, 0), (1, 1), (1, 9), (3, 2), (0, 7)],
    [-1, -1, -1, -1, -1],
    0],
    [[], [], [], [], []],
    [[(1, 3), (2, 2), (0, 3), (1, 6), (4, 8), (3, 3), (2, 6), (4, 10)],
    [-1, -1, -1, -1, -1],
    0],
    None,
    44]

def repeat_N_move(n, state):
    print(state)
    for _ in range(n):
        root = ExpeditionNode(state)
        node = UCT(root, 8000)
        print(node.move)
        node.parent.children_display()

if __name__ == '__main__':
    #run_games(1000)
    import random
    random.seed(11031987)
    #profile_mcts(200)
    run_mcts(4000, test)
    #repeat_N_move(10, test)
