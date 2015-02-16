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
        for _, game in self._state["games"].items():
            stats["games"].append(game.get_stats())

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