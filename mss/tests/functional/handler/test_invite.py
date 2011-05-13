# coding: utf-8
#!/usr/bin/env python

from mss.core.cache import get_cache
from mss.handler.invite import SendInviteHandler, AcceptInviteHandler, GetInviteHandler, SendEmailInviteHandler, AcceptEmailInviteHandler
from tornado.testing import AsyncHTTPTestCase
import tornado

class InviteHandlerTestCase(AsyncHTTPTestCase):
    
    def get_app(self):
        
        routes = [
            (r"/invite/send", SendInviteHandler),
            (r"/invite/accept", AcceptInviteHandler),
            (r"/invite/get.json", GetInviteHandler),
            (r"/invite/email/send", SendEmailInviteHandler),
            (r"/invite/email/accept", AcceptEmailInviteHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_send_context(self):
        pass