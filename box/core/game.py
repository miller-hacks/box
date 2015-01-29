# coding: utf-8
import uuid
from core.round import CollectPlayersRound, SolveExampleRound, FinalRound
from core.player import Player


def generate_game_code(length=4):
    return "q" * length


class Game(object):

    NAME = "base"

    STAGE_NEW = 0
    STAGE_RUNNING = 1
    STAGE_FINISHED = 2

    def __init__(self, code=None, rounds=None, players=None):
        self.uid = uuid.uuid4().hex
        self.code = code or generate_game_code()
        self.rounds = rounds or []
        self.players = players or []
        self.current_stage = self.STAGE_NEW
        self.current_round = None
        self.game_state = self.get_initial_game_state()

    def get_initial_game_state(self):
        return {}

    def is_new(self):
        return self.current_stage == self.STAGE_NEW

    def is_running(self):
        return self.current_stage == self.STAGE_RUNNING

    def is_finished(self):
        return self.current_stage == self.STAGE_FINISHED

    def to_new(self):
        self.current_stage = self.STAGE_NEW

    def to_running(self):
        self.current_stage = self.STAGE_RUNNING

    def to_finished(self):
        self.current_stage = self.STAGE_FINISHED

    def get_player(self, uid):
        if not uid:
            if not self.is_new():
                return None
            player = Player()
            self.add_player(player)
        else:
            player = None
            for p in self.players:
                if p.uid == uid:
                    player = p
                    break
        return player

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def get_current_round(self):
        return self.current_round

    def get_next_round(self):
        raise NotImplementedError()

    def run(self):
        if not self.is_new():
            return

        self.to_running()

        while True:
            try:
                self.current_round = self.rounds.pop(0)
            except IndexError:
                break
            self.current_round.run()

        self.to_finished()

    def set_state(self, data):
        pass

    def set_player_state(self, player, data):
        pass


class SolveGame(Game):
    """
    Simple game - the goal of each player is solving examples.
    Given an example such as "2 + 2 = ?" player must submit an
    answer. The faster player submits an answer the more points
    player receive.
    """

    NAME = "solve"

    EXAMPLES = (
        ("2 + 2 = ?", "4"),
        ("3 * 2 = ?", "6"),
        ("4 + 3 = ?", "7")
    )

    def set_player_state(self, player, data):
        player.set_state(data)

    def get_next_round(self):
        if self.is_new():
            self.current_round = CollectPlayersRound(self)
            self.rounds = [
                SolveExampleRound(self, props={"example": x[0], "answer": x[1]}) for x in self.EXAMPLES
            ]
        else:
            try:
                self.current_round = self.rounds.pop(0)
            except IndexError:
                self.current_round = FinalRound(self)

        return self.current_round
