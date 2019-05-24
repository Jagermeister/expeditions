from src.model.model import Expedition
from src.mcts.mcts_model import ExpeditionNode
from src.mcts.mcts import UCT

from colorama import init, Fore, Back, Style
init()
from termcolor import cprint, colored
from pyfiglet import figlet_format

import time
from src.model.player import Player

def run_games(n):
    game = Expedition()
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

def record_move_stats(stats, move, evalulation):
    action, (_, pull) = move
    stats['evaluation'].append(evalulation)
    if action == 'play':
        stats['play_card'] += 1
    else: 
        stats['play_discard'] += 1
    
    if pull == 'd':
        stats['pull_card'] += 1
    else:
        stats['pull_discard'] += 1

def run_mcts(n, modelState=None, userInput=False, verbose=True):
    model = None
    if modelState:
        model = Expedition.make_from_state(modelState, False)
    else:
        model = Expedition()
        model.setup()
    
    now = time.clock()
    move_stats = {
        'play_card': 0,
        'play_discard': 0,
        'pull_card': 0,
        'pull_discard': 0,
        'evaluation': []
    }
    while model.cardsInDeckCount:
        node = UCT(ExpeditionNode(model.state()), n)
        if verbose:
            print('___________________________________________')
            print('Turn:', int(model.turnPly/2), 'State:', model)
            print(Back.WHITE + Fore.RED, 'Selected Move:', end='')
            print(Style.RESET_ALL, end='')
            print(ExpeditionNode.move_display(node.move), Style.RESET_ALL, flush=True)

        if verbose: node.parent.children_display()
        model.play_move(node.move)
        record_move_stats(move_stats, node.move, node.reward/node.visits)
        if model.cardsInDeckCount:
            if userInput:
                print(model)
                p = model.player()
                o = Player.play_options(p[Player.handIndex], p[Player.boardIndex])
                for a in sorted(p[Player.handIndex], key=lambda c: (c[0], c[1])):
                    print(
                        '('+str(a[0])+','+ str('X' if a[1] < 3 else a[1]-1),
                        end=')  ')
                print()
                for i, a in enumerate(o):
                    print(
                        str(i)+'/'+str(8 + i)+':'
                        '('+str(a[0])+','+ str('X' if a[1] < 3 else a[1]-1),
                        end=')  ')
                print()
                a = int(input())
                action = 'discard' if a < 8 else 'play'
                play = p[Player.handIndex][a] if a < 8 else o[a-8]
                print(model.discard)
                a = input()
                a = 0 if a == '' else int(a)
                pull = 'd' if a == 0 else a
                print('>>', (action, (play, pull)))
                model.play_move((action, (play, pull)))
            else:
                move = model.play_random_turn()
                if verbose:
                    print('\r\n' + Back.RED + Fore.WHITE +
                        'Opponent\'s move:',
                        ExpeditionNode.move_display(move),
                        Style.RESET_ALL, flush=True)

    print(model.winner,
        Player.board_score(model.players[0][Player.boardStateIndex]),
        Player.board_score(model.players[1][Player.boardStateIndex])
    )
    print(move_stats)
    print(time.clock() - now, flush=True)
    return model.winner

def profile(function):
    import cProfile, pstats, io
    pr = cProfile.Profile()
    pr.enable()
    function()
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    sortby = 'tottime'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

# 5000 games in 14s w   1849770867 ply: 'p1': 2436, 'p2': 2499, 'tie': 65
test = [
    792280796199869815, 0,
    [[(4, 0), (0, 9), (3, 10), (3, 0), (1, 1), (1, 9), (3, 2), (0, 7)],
    [-1, -1, -1, -1, -1], 0],
    [[], [], [], [], []],
    [[(1, 3), (2, 2), (0, 3), (1, 6), (4, 8), (3, 3), (2, 6), (4, 10)],
    [-1, -1, -1, -1, -1], 0],
    None, 44]

def repeat_N_move(n, state):
    print(state)
    for _ in range(n):
        root = ExpeditionNode(state)
        node = UCT(root, 8000)
        print(node.move)
        node.parent.children_display()

if __name__ == '__main__':
    #Introduction
    cprint(figlet_format('Expeditions!', font='big'), 'yellow', 'on_blue', attrs=['bold'])
    #Game settings explained
    from model.config import Config
    Config = Config()
    print(Config)

    #Run Game

    #run_games(1000)
    #import random
    #random.seed(11031987)
    #profile_mcts(200)

    iterations = 2000
    run_mcts(iterations)

    #result = 0
    #games = 20
    #for _ in range(games):
    #    result += run_mcts(iterations, None, False, False)
    #print(result, "/", games)

    ##repeat_N_move(10, test)