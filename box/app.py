# coding: utf-8

from tornado.ioloop import IOLoop
import tornado.web
import os
from tornado.options import options
from handlers import MainHandler, ApiHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/api", ApiHandler),
        ]
        settings = dict(
            cookie_secret=os.environ.get("BOX_COOKIE_SECRET", "secret"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def run():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8000)
    IOLoop.instance().start()

if __name__ == "__main__":
    run()