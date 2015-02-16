# encoding: utf-8
import tornado.web
import json


class BaseJsonResponseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseJsonResponseHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'application/json; charset="utf-8"')


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header('Content-Type', 'text/html; charset="utf-8"')
        self.write("""
            <a href="/new/">new game</a><br />
            <a href="/game/qqqq/">game</a><br />
            <a href="/stats/">stats</a>
        """)


class NewGameHandler(BaseJsonResponseHandler):

    def get(self):
        game = self.application.state.new_game()
        self.finish(json.dumps({
            "code": game.code
        }))


class GameHandler(BaseJsonResponseHandler):

    def get(self, code):
        game = self.application.state.get_game(code)
        if not game:
            self.set_status(404)
            self.finish(json.dumps({"error": "game not found"}))
        else:
            uid = self.get_argument("uid", None)
            player = game.get_player(uid)

            action = self.get_argument("action", None)
            game.current_round.data_received(player, {"action": action})

            self.finish(json.dumps({
                "players": [x.name for x in game.players],
                "me": {
                    "uid": player.uid,
                    "name": player.name
                }
            }))


class StatsHandler(BaseJsonResponseHandler):

    def get(self):
        app_state = self.application.state.get_stats()
        self.finish(json.dumps(app_state))
