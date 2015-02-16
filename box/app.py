# coding: utf-8

from tornado.ioloop import IOLoop
import tornado.web
from tornado.options import options
from handlers import MainHandler, GameHandler, NewGameHandler, StatsHandler
from core.game import SolveGame


class State(object):

    def __init__(self, application):
        self.application = application
        self._state = {
            "games": {}
        }

    def new_game(self):
        game = SolveGame()
        game.get_next_round()
        self.add_game(game)
        return game

    def add_game(self, game):
        self._state["games"][game.code] = game

    def remove_game(self, game):
        if game.code in self._state["games"]:
            del self._state["games"][game.code]

    def get_game(self, code):
        return self._state["games"].get(code)

    def get_stats(self):
        stats = {
            "games": []
        }
<<<<<<< HEAD
        for game_code, game in self._state["games"].items():
            current_round_stats = game.current_round.get_render_data() if game.current_round else None
            game_stats = {
                "players": [],
                "code": game.code,
                "current_round": current_round_stats
            }
            for player in game.players:
                game_stats["players"].append({
                    "uid": player.uid,
                    "name": player.name
                })
            stats["games"].append(game_stats)
=======
        for _, game in self._state["games"].items():
            stats["games"].append(game.get_stats())
>>>>>>> 36516d01c808145a4882dba61266a8ccfe214259
        return stats


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/new/", NewGameHandler),
            (r"/game/([^/]+)/", GameHandler),
            (r"/stats/", StatsHandler)
        ]
        settings = {}
        tornado.web.Application.__init__(self, handlers, **settings)
        self.state = State(self)


def run():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8000)
    IOLoop.instance().start()

if __name__ == "__main__":
    run()