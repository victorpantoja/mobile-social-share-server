# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.user import CreateLoginHandler, LoginHandler
from mss.models.user import User
from tornado.testing import AsyncHTTPTestCase
from nose import with_setup

import tornado
from mss.tests.functional.utils import create_user

class UserHandlerTestCase(AsyncHTTPTestCase):
    
    session = get_session()
    
    def get_app(self):
        
        routes = [
            (r"/login", LoginHandler),
            (r"/login/create", CreateLoginHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_create_user(self):
        self.http_client.fetch(self.get_url('/login/create')+'?username=should-be-username&firstName=test_create_user&lastName=should-be-last-name&gender=M' , self.stop)
                
        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Account Created! Verify you email account"}')

        user_db = self.session.query(User).filter(User.username=='should-be-username').first()
        user_db.delete()


    def test_create_existent_user(self):
        
        user = create_user()
                        
        self.http_client.fetch(self.get_url('/login/create')+'?username=%s&firstName=%s&lastName=%s&gender=M' %(user.username, user.first_name, user.last_name) , self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "Username already exists."}')
        
        user.delete()
