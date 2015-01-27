# coding: utf-8


def generate_game_code(length=4):
    return "q" * length


class Game(object):

    STAGE_NEW = 0
    STAGE_RUNNING = 1
    STAGE_FINISHED = 2

    def __init__(self, code=None, players=None):
        self.code = code or generate_game_code()
        self.players = players or []
        self.current_stage = self.STAGE_NEW

    def is_new(self):
        return self.current_stage == self.STAGE_NEW

    def is_running(self):
        return self.current_stage == self.STAGE_RUNNING

    def is_finished(self):
        return self.current_stage == self.STAGE_FINISHED
