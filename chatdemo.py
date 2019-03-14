# coding:utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler

define("port", default=2222, type=int)

class IndexHandler(RequestHandler):
    def get(self):
        self.set_cookie('user', self.get_argument('user'))
        self.render("chat-client.html")

class ChatHandler(WebSocketHandler):
    userid = {}
    uuu = ''
    def open(self):
        self.uuu = self.get_cookie('user')
        if self.uuu not in self.userid:
            self.userid[self.uuu] = self
        for us in self.userid:
            self.userid[us].write_message(u"[%s]-[%s]-in room" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        if '&' in message:
            new_message = message.split('&')
            self.write_message(u"[%s]-[%s]-say: %s" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
            if new_message[-1] in self.userid:
                self.userid[new_message[-1]].write_message(u"[%s]-[%s]-say: %s" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
            else:
                self.write_message(u"[%s]-[%s]-say: %s" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), u"%s is not in room" % new_message[-1]))

        #for us in self.userids:
            #us.write_message(u"[%s]-[%s]-say: %s" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        del self.userid[self.uuu]
        for us in self.userid:
            self.userid[us].write_message(u"[%s]-[%s]-out room" % (self.uuu, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True,
        cookie_secret = "lkjwlkejrlkwejrwklejrwerwerwerwerwerqwkejrkwjerkj/324="
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(int(options.port), "0.0.0.0")
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()
