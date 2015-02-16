# coding: utf-8
import uuid
from core.round import CollectPlayersRound, SolveExampleRound, FinalRound
from core.player import Player


def generate_game_code(length=4):
    return "q" * length


class Game(object):

    NAME = "base"

    def __init__(self, code=None, rounds=None, players=None):
        self.uid = uuid.uuid4().hex
        self.code = code or generate_game_code()
        self.rounds = rounds or []
        self.players = players or []
        self.current_round = None
        self.state = self.get_initial_state()

    def get_initial_state(self):
        return {}

    def get_player(self, uid):
        if not uid:
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

    def set_state(self, data):
        pass

    def set_player_state(self, player, data):
        pass

    def get_stats(self):
        stats = {
            "players": [],
            "code": self.code,
            "current_round": self.current_round.get_render_data() if self.current_round else None
        }
        for player in self.players:
            stats["players"].append({
                "uid": player.uid,
                "name": player.name
            })
        stats["players_count"] = len(stats["players"])
        return stats


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

    # noinspection PyTypeChecker
    def get_next_round(self):
        if not self.rounds:
            self.rounds = [CollectPlayersRound(self)]
            for example in self.EXAMPLES:
                self.rounds.append(
                    SolveExampleRound(self, props={"example": example[0], "answer": example[1]})
                )
            self.rounds.append(FinalRound(self))
        try:
            self.current_round = self.rounds.pop(0)
        except IndexError:
            raise Exception("This should not be reached")

        self.current_round.run()
        return self.current_round
