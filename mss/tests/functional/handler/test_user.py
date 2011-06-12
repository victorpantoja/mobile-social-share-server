# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.user import CreateLoginHandler, LoginHandler, UserHandler, UserSearchHandler
from mss.models.user import User
from tornado.testing import AsyncHTTPTestCase
from nose import with_setup

import tornado, simplejson
from mss.tests.functional.utils import create_user, create_logged_user
from mss.core.cache.util import get_cache

class UserHandlerTestCase(AsyncHTTPTestCase):
    
    session = get_session()
    
    def get_app(self):
        
        routes = [
            (r"/login", LoginHandler),
            (r"/login/create", CreateLoginHandler),
            (r"/user.json", UserHandler),
            (r"/search/users.json", UserSearchHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_can_login(self):
        
        user = create_user(username='test_can_login')
        
        self.http_client.fetch(self.get_url('/login')+'?username=%s&password=should-be-password' % user.username , self.stop)
                
        response = self.wait()
                
        cache = get_cache()
        username = cache.get(simplejson.loads(response.body)['msg'])
        
        assert username == user.username
        
        user.delete()
    
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
        
    def test_get_user_myself(self):
        user = create_logged_user()
        
        self.http_client.fetch(self.get_url('/user.json?auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, simplejson.dumps({'user':user.as_dict()}))
        
        user.delete()
        
    def test_get_other_user(self):
        user = create_logged_user()
        user2 = create_user("test_get_other_user", "test_get_other_user", "test_get_other_user")
        
        self.http_client.fetch(self.get_url('/user.json?username=%s&auth=should-be-user-auth' % user2.username), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, simplejson.dumps({'user':user2.as_dict()}))
        
        user.delete()
        user2.delete()
        
    def test_get_other_inexistent_user(self):
        user = create_user()
        
        self.http_client.fetch(self.get_url('/user.json?username=anybody&auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, simplejson.dumps({"status": "error", "msg": "User not found."}))
        
        user.delete()
        
    def test_search_user(self):
        user = create_user()
        user2 = create_user("test_get_other_user-2", "test_get_other_user-2", "test_get_other_user-2")
        user3 = create_user("test_get_other_user-3", "test_get_other_user-3", "test_get_other_user-3")

        self.http_client.fetch(self.get_url('/search/users.json?username=%s&auth=should-be-user-auth' % "test_"), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, simplejson.dumps({'users':[user2.as_dict(),user3.as_dict()]}))

        user.delete()
        user2.delete()
        user3.delete()
