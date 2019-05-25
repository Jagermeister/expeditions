""" Transition views based on game state """

from enum import Enum

from src.model.gamemanager import GamesManager
from src.view.terminal.viewphase.examinephase import ExaminePhase
from src.view.terminal.viewphase.playphase import PlayPhase
from src.view.terminal.viewphase.setupphase import SetupPhase


class GameManagerViewState(Enum):
    """ Game Manager View State """
    INIT = 0
    SETUP = 1
    PLAY = 2
    EXAMINE = 3

class GameManagerView():
    """ Transition between viewphases """

    def __init__(self):
        self.game_manager = GamesManager()
        self.state = GameManagerViewState.INIT
        self.phase = None

        self.games_to_play = 10
        self.games = 0
        self.game_score_by_player = {}

    def handle_events(self):
        """ Issue and process user events """
        if self.phase:
            self.phase.handle_events()

    def __state_update_init(self):
        """ Transition to INIT state """
        self.state = GameManagerViewState.SETUP
        self.phase = SetupPhase(self.game_manager)

    def __state_update_play(self):
        """ Transition to PLAY state """
        self.state = GameManagerViewState.PLAY
        self.phase = PlayPhase(self.game_manager)
        for i in range(self.game_manager.game.player_count):
            self.game_score_by_player[i] = 0

        print(f'Game {self.games + 1} - Play!')

    def __state_to_play_next(self):
        """ Transition to PLAY state again """
        self.games += 1
        self.game_manager.game.state_display()

        reward = self.game_manager.game.reward()
        if self.game_manager.game.player_count == 1:
            player_active = 0
        else:
            turn_ply = self.game_manager.game.turn_ply
            player_count = self.game_manager.game.player_count
            player_active = 0 if turn_ply % player_count else 1

        if reward == 1:
            print('Winner: Player {}'.format(player_active + 1))
            self.game_score_by_player[player_active] += 1
        elif reward == 0.5:
            print('Tied!')
            for key in self.game_score_by_player:
                self.game_score_by_player[key] += 0.5
        else:
            print('Player 1 Lost')
            for key in self.game_score_by_player:
                if key != player_active:
                    self.game_score_by_player[key] += 1

        if self.games < self.games_to_play:
            self.phase = PlayPhase(self.game_manager)
            self.game_manager.game.reset()

        print('Game {} - Score By Players: {}\n\r'.format(
            self.games,
            ', '.join([
                str(self.game_score_by_player[key]) for key in self.game_score_by_player])
        ), flush=True)

        if self.games == self.games_to_play:
            self.__state_to_examine()

    def __state_to_examine(self):
        """ Transition to EXAMINE state """
        input('Game Over')
        self.state = GameManagerViewState.EXAMINE
        self.phase = ExaminePhase(self.game_manager)


    def update(self):
        """ Update internal state """
        if self.state == GameManagerViewState.INIT:
            self.__state_update_init()
        elif self.state == GameManagerViewState.SETUP and self.phase.is_complete:
            self.__state_update_play()
        elif self.state == GameManagerViewState.PLAY and self.phase.is_complete:
            self.__state_to_play_next()

        self.phase.update()

    def display(self):
        """ Visual display of view phase state """
        self.phase.display()

    def play_turn(self):
        """ Delegate playing to game_manager """
        self.game_manager.play_turn()
