# coding: utf-8
#!/usr/bin/env python

from datetime import datetime
from mss.core.meta import get_session
from mss.handler.friendship import CreateFriendshipHandler, GetFriendshipsHandler
from mss.models.friendship import Friendship
from tornado.testing import AsyncHTTPTestCase
from nose import with_setup

import tornado
from mss.models.user import User

class FriendshipHandlerTestCase(AsyncHTTPTestCase):
    
    session = get_session()
    
    def get_app(self):
        
        routes = [
            (r"/friendship/create", CreateFriendshipHandler),
            (r"/friendship/get.json", GetFriendshipsHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_create_friendship(self):
        
        user = User()
        user.last_name = 'should-be-last-name-1'
        user.first_name = 'test_create_friendship-1'
        user.username = 'should-be-username-1'
        user.created = datetime.now()
        user.last_login = datetime.now()
        user.password = 'should-be-password-1'
        user.save()
        
        #TODO - testar user.create()
        
        user2 = User()
        user2.last_name = 'should-be-last-name-2'
        user2.first_name = 'test_create_friendship-2'
        user2.username = 'should-be-username-2'
        user2.created = datetime.now()
        user2.last_login = datetime.now()
        user2.password = 'should-be-password-2'
        user2.save()
        
        self.http_client.fetch(self.get_url('/friendship/create'), self.stop)
                
        response = self.wait()
        
        try:
            self.failIf(response.error)
            self.assertEqual(response.body, '{"status": "ok", "msg": "User Fulano is now your friend!"}')
        except Exception, e:
            raise e
        finally:
            friendship_db = self.session.query(Friendship).filter(Friendship.user_id=='should-be-username').first()
            friendship_db.delete()