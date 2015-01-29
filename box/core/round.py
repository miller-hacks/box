# coding: utf-8
import uuid


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
        if data["action"] == 'start':
            self.game.set_player_state(player, {"ready": True})
        elif data["action"] == 'name':
            self.game.set_player_state(player, {"name": data["payload"]})

    def get_state_data(self):
        return {
            "players": [x.name for x in self.game.players]
        }


class SolveExampleRound(Round):

    def data_received(self, player, data):
        if data["action"] == 'answer':
            current_score = player.state.get("score", 0)

            if self.props["answer"] == data["payload"]:
                new_score = current_score + 10
            else:
                new_score = current_score - 1

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