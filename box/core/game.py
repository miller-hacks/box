# coding: utf-8
import uuid


def generate_game_code(length=4):
    return "q" * length


class Game(object):

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

    def add_player(self, player):
        if not self.is_new():
            return False
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

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