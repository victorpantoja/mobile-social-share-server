# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.invite import SendInviteHandler, AcceptInviteHandler, GetInviteHandler, SendEmailInviteHandler, AcceptEmailInviteHandler
from mss.models.invite import Invite
from mss.models.invite_email import InviteEmail
from mss.models.friendship import Friendship
from mss.tests.functional.utils import create_logged_user, create_user, create_invite
from tornado.testing import AsyncHTTPTestCase

import tornado, hashlib

class InviteHandlerTestCase(AsyncHTTPTestCase):
    
    session = get_session()
    
    def get_app(self):
        
        routes = [
            (r"/invite/send", SendInviteHandler),
            (r"/invite/accept", AcceptInviteHandler),
            (r"/invite/get.json", GetInviteHandler),
            (r"/invite/email/send", SendEmailInviteHandler),
            (r"/invite/email/accept", AcceptEmailInviteHandler)
        ]
        
        return tornado.web.Application(routes)
    
    def test_send_invite(self):
        user = create_logged_user()
        user2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')

        self.http_client.fetch(self.get_url('/invite/send?friend_id=%s&auth=should-be-user-auth' % user2.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Your invited has been sent!"}')
        
        invite = self.session.query(Invite).filter(Invite.user_id==user.id).first()
        
        assert invite.user_id == user.id
        assert invite.friend_id == user2.id
        
        invite.delete()
        user.delete()
        user2.delete()
    
    def test_accept_invite(self):
        user = create_logged_user()
        friend = create_user(last_name = 'should-be-last-name-2', first_name = 'test_create_friendship-2',  username = 'should-be-username-2')

        invite = create_invite(user, friend)

        self.http_client.fetch(self.get_url('/invite/accept?invite_id=%s&auth=should-be-user-auth' % invite.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "User test_create_friendship-2 is now your friend!"}')
    
        invite = self.session.query(Invite).filter(Invite.user_id==user.id).first()
        
        self.assertEqual(invite, None)
        
        friendship = self.session.query(Friendship).filter(Friendship.user_id==user.id).first()

        assert friendship.user_id == user.id
        assert friendship.friend_id == friend.id
        
        friendship.delete()
        user.delete()
    
    def test_get_invites(self):
        user = create_logged_user()
        friend1 = create_user(last_name = 'should-be-last-name-1', first_name = 'test_get_invites-1',  username = 'should-be-username-friend-1')
        friend2 = create_user(last_name = 'should-be-last-name-2', first_name = 'test_get_invites-2',  username = 'should-be-username-friend-2')

        invite1 = create_invite(user, friend1)
        invite2 = create_invite(user, friend2)
        
        self.http_client.fetch(self.get_url('/invite/get.json?auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"invite": [{"username": "should-be-username-friend-1", "first_name": "test_get_invites-1", "last_name": "should-be-last-name-1"}, {"username": "should-be-username-friend-2", "first_name": "test_get_invites-2", "last_name": "should-be-last-name-2"}]}')
        
        invite1.delete()
        invite2.delete()
        user.delete()
        friend1.delete()
        friend2.delete()
        
    def test_send_email_invite(self):
        user = create_logged_user()
        
        email = "victor.pantoja@gmil.com"
        
        m = hashlib.md5()
        m.update("%s%s" % (email,user.id))
        
        code = m.hexdigest()
        self.http_client.fetch(self.get_url('/invite/email/send?email=%s&auth=should-be-user-auth' % email), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Your invite has been sent."}')
        
        invite_email = self.session.query(InviteEmail).filter(InviteEmail.code==code).first()

        invite_email.delete()
        user.delete()
    
    def test_accept_email_invite(self):
        pass