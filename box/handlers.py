# encoding: utf-8
import tornado.web
import json


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("I work, baby!")


class ApiHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(ApiHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'application/json; charset="utf-8"')

    def get(self):
        self.write(json.dumps({}))
