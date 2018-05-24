from model.game.tictactoe.TTTGame import TTTGame
from model.game.tictactoe.agent.randomagent import RandomAgent


class GamesManager(object):

    def __init__(self):
        self.game = None
        self.games = {}
        self.agents = {}
        self.game_add()

    def game_add(self):
        game_name = 'Tic Tac Toe'
        self.games[game_name] = TTTGame
        self.agents[game_name] = RandomAgent

    def game_select(self, game_name):
        self.game = self.games[game_name]()
        agent = self.agents[game_name]
        self.game.player_add(agent(self.game))
        self.game.player_add(agent(self.game))

    def game_play(self):
        g = self.game
        while not g.is_terminal:
            for p in g.players:
                if not g.is_terminal:
                    g.move_play(p.move_from_state())
        print(g.is_terminal, g.board)