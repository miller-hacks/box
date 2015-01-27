# coding: utf-8


class Round(object):
    """
    Abstract class to describe Game round
    """
    def __init__(self, time_limit=None):
        self.time_limit = time_limit

    def run(self):
        raise NotImplementedError("run method must be implemented in subclasses of Round")

