# coding: utf-8
import uuid
import names


def generate_player_name():
    return names.get_first_name()


class Player(object):

    def __init__(self, name=None):
        self.uid = uuid.uuid4().hex
        self.name = name or generate_player_name()
        self.score = 0
        self.state = {}

    def set_state(self, data):
        self.state.update(data)
