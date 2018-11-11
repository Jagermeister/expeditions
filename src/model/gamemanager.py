from copy import deepcopy

from model.game.agent.agent import Agent

from model.game.tictactoe.TTTGame import TTTGame
from model.game.tictactoe.agent.randomagent import RandomAgent
from model.game.tictactoe.agent.rulefirstavailableagent import RuleFirstAvailableAgent
from model.game.tictactoe.agent.manualagent import ManualAgent
from model.game.tictactoe.agent.mctsagent import TTTMCTSAgent

from model.game.expedition.ExpeditionGame import ExpeditionGame
from model.game.expedition.agent.manualagent import ManualAgent as ExpeditionManualAgent

from model.game.guessnumber.GuessGame import GuessGame
from model.game.guessnumber.agent.manualagent import ManualAgent as GuessNumberManualAgent

class GamesManager(object):

    def __init__(self):
        self.game = None
        self.games = {}
        self.agents = {}
        self.game_add()
        self.game_states = []

    def game_add(self):
        self._game_add_with_players(
            TTTGame,
            [RandomAgent, RuleFirstAvailableAgent, TTTMCTSAgent, ManualAgent]
        )

        self._game_add_with_players(
            ExpeditionGame,
            [ExpeditionManualAgent]
        )

        self._game_add_with_players(
            GuessGame,
            [GuessNumberManualAgent]
        )

    def _game_add_with_players(self, game, players):
        self.games[game.name] = game
        self.agents[game.name] = {}
        for p in players:
            self.agents[game.name][p.name] = p

    ###
    #   GAMES
    ###
    def games_available(self):
        return list(self.games.keys())

    def game_select_by_name(self, game_name):
        self.game_select(self.games[game_name])

    def game_select(self, game):
        self.game = game()

    ###
    #   PLAYERS
    ###
    @property
    def is_player_needed(self):
        return self.player_count() < self.game.player_count

    def player_count(self):
        return len(self.game.players)

    def players_available(self):
        return list(self.agents[self.game.name].keys())

    def player_add_by_name(self, player_name):
        self.player_add(self.agents[self.game.name][player_name](self.game))

    def player_add(self, player):
        assert isinstance(player, Agent)
        self.game.player_add(player)

    @property
    def is_terminal(self):
        return self.game.is_terminal

    def play_turn(self):
        g = self.game
        for p in g.players:
            if not g.is_terminal:
                g.move_play(p.move_from_state())
                self.state_save()

    def state_save(self):
        self.game_states.append(
            deepcopy(self.game.state)
        )

    def game_play(self):
        while not self.game.is_terminal:
            self.play_turn()