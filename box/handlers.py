# encoding: utf-8
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("I work, baby!")


class GameHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(GameHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'application/json; charset="utf-8"')

    def get(self, code):
        game = self.application.state.get_game(code)
        if not game:
            self.set_status(404)
            self.finish(json.dumps({}))
        else:
            self.finish(json.dumps({
                "players": [x.name for x in game.players]
            }))
