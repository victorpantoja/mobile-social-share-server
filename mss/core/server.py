# coding: utf-8
#!/usr/bin/env python

from mss.core.daemon import Daemon
from mss.handler.context import ContextHandler
from mss.handler.facebook import CanvasHandler
from mss.handler.friendship import CreateFriendshipHandler, GetFriendshipsHandler, RemoveFriendshipsHandler
from mss.handler.invite import SendInviteHandler, GetInviteHandler, SendEmailInviteHandler, AcceptInviteHandler, AcceptEmailInviteHandler
from mss.handler.user import LoginHandler, CreateLoginHandler

from tornado.options import options

from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler, RequestHandler, HTTPError
from tornado.ioloop import IOLoop

import logging


COOKIE_SECRET = "29NbhyfgaA092ZkjMbNvCx06789jdA8iIlLqz7d1D9c8"

class MSSServer(Daemon):
    
    def __init__(self):
        
        return Daemon.__init__(self, options.pidfile)

    def run(self):
        
        routes = [
            (r"/media/(.*)", StaticFileHandler, {"path": options.media_dir}),
            (r"/canvas/", CanvasHandler),
            (r"/context", ContextHandler),
            (r"/login", LoginHandler),
            (r"/login/create", CreateLoginHandler),
            (r"/friendship/create", CreateFriendshipHandler),
            (r"/friendship/get.json", GetFriendshipsHandler),
            (r"/friendship/remove", RemoveFriendshipsHandler),
            (r"/invite/send", SendInviteHandler),
            (r"/invite/accept", AcceptInviteHandler),
            (r"/invite/get.json", GetInviteHandler),
            (r"/invite/email/send", SendEmailInviteHandler),
            (r"/invite/email/accept", AcceptEmailInviteHandler),
        ]
    
        application = Application(routes, cookie_secret=COOKIE_SECRET)
                
        http_server =   HTTPServer(application,xheaders=True)
        http_server.listen(options.port)
                
        logging.info("mobile-social-share server START! listening port %s " % options.port)
        
        IOLoop.instance().start()
        