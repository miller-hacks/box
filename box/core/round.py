# coding: utf-8
import uuid
from tornado.ioloop import IOLoop
import time


class Round(object):
    """
    Abstract class to describe Game round
    """
    def __init__(self, game, time_limit=None, props=None):
        self.uid = uuid.uuid4().hex
        self.game = game
        self.time_limit = time_limit
        self.state = {}
        self.props = props or {}

    def run(self):
        pass

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_render_data(self):
        return {
            "component": self.__class__.__name__,
            "state": self.get_state_data()
        }

    def get_state_data(self):
        return {}

    def data_received(self, player, data):
        """
        Handle data from player
        """
        pass


class CollectPlayersRound(Round):

    def data_received(self, player, data):
        if data["action"] == 'ready':
            self.game.get_next_round()

    def get_state_data(self):
        return {
            "players": [x.name for x in self.game.players]
        }


class SolveExampleRound(Round):

    def run(self):
        self.finish = IOLoop.current().add_timeout(time.time() + 20, self.on_finish)

    def on_finish(self):
        self.game.get_next_round()

    def data_received(self, player, data):
        if data["action"] == 'answer':
            current_score = player.state.get("score", 0)

            if self.props["answer"] == data["payload"]:
                new_score = current_score + 10
            else:
                new_score = current_score - 5

            self.game.set_player_state(player, {"score": new_score})

    def get_state_data(self):
        return {
            "example": self.props["example"]
        }


class FinalRound(Round):

    def get_state_data(self):
        data = {
            "stats": []
        }
        for player in self.game.players:
            data["stats"].append({
                "player": player.name,
                "score": player.state.get("score", 0)
            })

        return data