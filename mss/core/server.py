# coding: utf-8
#!/usr/bin/env python

from mss.core.daemon import Daemon
from mss.handler.application import ApplicationHandler, SubscribeHandler
from mss.handler.context import ContextHandler, WebViewHandler, ContextTestHandler
from mss.handler.facebook import CanvasHandler
from mss.handler.friendship import GetFriendshipsHandler, RemoveFriendshipsHandler
from mss.handler.invite import SendInviteHandler, GetInviteHandler, SendEmailInviteHandler, AcceptInviteHandler, AcceptEmailInviteHandler, GetInvitationHandler
from mss.handler.status import StatusHandler
from mss.handler.user import LoginHandler, CreateLoginHandler, UserHandler, UserSearchHandler

from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler
from tornado.ioloop import IOLoop

import logging
from mss.handler.maps import MapsHandler

COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"


class MSSServer(Daemon):

    def __init__(self):

        return Daemon.__init__(self, options.pidfile)

    def run(self):

        routes = [
            (r"/media/(.*)", StaticFileHandler, {"path": options.media_dir}),
            (r"/applications.json", ApplicationHandler),
            (r"/application/subscribe", SubscribeHandler),
            (r"/canvas/", CanvasHandler),
            (r"/webview/", WebViewHandler),
            (r"/context", ContextHandler),
            (r"/context/callback_url", ContextTestHandler),
            (r"/login", LoginHandler),
            (r"/login/create", CreateLoginHandler),
            (r"/maps", MapsHandler),
            (r"/friendship/get.json", GetFriendshipsHandler),
            (r"/friendship/remove", RemoveFriendshipsHandler),
            (r"/invite/send", SendInviteHandler),
            (r"/invite/accept", AcceptInviteHandler),
            (r"/invite/get.json", GetInviteHandler),
            (r"/invite/email/send", SendEmailInviteHandler),
            (r"/invite/email/accept", AcceptEmailInviteHandler),
            (r"/invitation/get.json", GetInvitationHandler),
            (r"/user.json", UserHandler),
            (r"/search/users.json", UserSearchHandler),
            (r"/status", StatusHandler),
        ]

        application = Application(routes, cookie_secret=COOKIE_SECRET)

        http_server = HTTPServer(application, xheaders=True)
        http_server.listen(options.port)

        logging.info("mobile-social-share server START! listening port %s " % options.port)

        IOLoop.instance().start()
