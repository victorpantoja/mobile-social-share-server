# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.friendship import CreateFriendshipHandler, GetFriendshipsHandler, RemoveFriendshipsHandler
from mss.models.friendship import Friendship
from tornado.testing import AsyncHTTPTestCase
from nose import with_setup

import tornado
from mss.tests.functional.utils import create_logged_user, create_user, create_friendship

class FriendshipHandlerTestCase(AsyncHTTPTestCase):
    
    session = get_session()
    
    def get_app(self):
        
        routes = [
            (r"/friendship/create", CreateFriendshipHandler),
            (r"/friendship/get.json", GetFriendshipsHandler),
            (r"/friendship/remove", RemoveFriendshipsHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_create_friendship(self):
        
        user = create_logged_user()
        user2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')
        
        self.http_client.fetch(self.get_url('/friendship/create?friend_id=%s&auth=should-be-user-auth' % user2.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "User test_create_friendship-2 is now your friend!"}')
        friendship_db = self.session.query(Friendship).filter(Friendship.user_id==user.id).first()
        friendship_db.delete()
        
        user.delete()
        user2.delete()
        
    def test_create_friendship_myself(self):
        
        user = create_logged_user()
    
        self.http_client.fetch(self.get_url('/friendship/create?friend_id=%s&auth=should-be-user-auth' % user.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "You cannot be a friend of yourself!"}')
        
        user.delete()
        
        
    def test_friend_not_found(self):
        
        user = create_logged_user()
        
        self.http_client.fetch(self.get_url('/friendship/create?friend_id=0&auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "User not found."}')
        
        user.delete()
        
    def test_create_duplicate_friendship(self):
        
        user = create_logged_user()
        user2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')
        
        friendship = create_friendship(user, user2)
        
        self.http_client.fetch(self.get_url('/friendship/create?friend_id=%s&auth=should-be-user-auth' % user2.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "You and %s are already friend!"}' % user2.first_name)

        friendship.delete()
        user.delete()
        user2.delete()
        
    def test_get_friendship(self):
        
        user = create_logged_user()
        user2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')
        user3 = create_user(last_name = 'should-be-last-name-3', first_name = 'test_create_friendship-3',  username = 'should-be-username-3')
        
        friendship = create_friendship(user, user2)
        friendship2 = create_friendship(user, user3)

        
        self.http_client.fetch(self.get_url('/friendship/get.json?auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"friend": [{"username": "should-be-username-2", "first_name": "test_create_friendship-2", "last_name": "should-be-last-name-2"}, {"username": "should-be-username-3", "first_name": "test_create_friendship-3", "last_name": "should-be-last-name-3"}]}')

        friendship.delete()
        friendship2.delete()
        user3.delete()
        user2.delete()
        user.delete()
        
    def test_remove_friendship(self):
        
        user = create_logged_user()
        user2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')
        
        create_friendship(user, user2)
        
        self.http_client.fetch(self.get_url('/friendship/remove?friend_id=%s&auth=should-be-user-auth' % user2.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Your friendship has been removed!"}')
        friendship_db = self.session.query(Friendship).filter(Friendship.user_id==user.id).first()
        
        self.assertEqual(friendship_db, None)

        user.delete()
        user2.delete()

    def test_remove_myself_friendship(self):
        
        user = create_logged_user()
        
        self.http_client.fetch(self.get_url('/friendship/remove?friend_id=%s&auth=should-be-user-auth' % user.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "Do you hate yourself?!"}')

        user.delete()
        
    def test_remove_inexistent_friendship(self):
        
        user = create_logged_user()
        
        self.http_client.fetch(self.get_url('/friendship/remove?friend_id=0&auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "This user are not your friend!"}')

        user.delete()
        