# coding: utf-8
import uuid


class Round(object):
    """
    Abstract class to describe Game round
    """
    def __init__(self, time_limit=None):
        self.uid = uuid.uuid4().hex
        self.time_limit = time_limit
        self.state = {}

    def run(self):
        raise NotImplementedError("run method must be implemented in subclasses of Round")

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def data_received(self, game, player, data):
        """
        Handle data from player
        """
        return
