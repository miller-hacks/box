# coding: utf-8

from tornado.ioloop import IOLoop
import tornado.web
import os
from tornado.options import options
from handlers import MainHandler, GameHandler, NewGameHandler
from core.game import SolveGame


class State(object):

    def __init__(self, application):
        self.application = application
        self._state = {
            "games": {}
        }

    def new_game(self):
        game = SolveGame()
        self.add_game(game)
        return game

    def add_game(self, game):
        self._state["games"][game.code] = game

    def remove_game(self, game):
        if game.code in self._state["games"]:
            del self._state["games"][game.code]

    def get_game(self, code):
        return self._state["games"].get(code)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/new/", NewGameHandler),
            (r"/game/([^/]+)/", GameHandler),
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