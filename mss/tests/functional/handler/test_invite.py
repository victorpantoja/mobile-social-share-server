# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.invite import SendInviteHandler, AcceptInviteHandler, GetInviteHandler, SendEmailInviteHandler, AcceptEmailInviteHandler
from mss.models.invite import Invite
from mss.models.invite_email import InviteEmail
from mss.models.friendship import Friendship
from mss.tests.functional.utils import create_logged_user, create_user, create_invite, create_invite_email, create_friendship
from tornado.testing import AsyncHTTPTestCase

import tornado, hashlib, simplejson

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
        user2 = create_user(last_name = 'test_send_invite', first_name = 'test_send_invite',  username = 'test_send_invite')

        self.http_client.fetch(self.get_url('/invite/send?username=%s&auth=should-be-user-auth' % user2.username), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Your invite has been sent."}')
        
        invite = self.session.query(Invite).filter(Invite.user_id==user.id).first()
        
        assert invite.user_id == user.id
        assert invite.friend_id == user2.id
        
        invite.delete()
        user.delete()
        user2.delete()
    
    def test_accept_invite(self):
        user = create_logged_user()
        friend = create_user(last_name = 'test_accept_invite', first_name = 'test_accept_invite',  username = 'test_accept_invite')

        invite = create_invite(user, friend)

        self.http_client.fetch(self.get_url('/invite/accept?invite_id=%s&auth=should-be-user-auth' % invite.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "User test_accept_invite is now your friend!"}')
    
        invite = self.session.query(Invite).filter(Invite.user_id==user.id).first()
        
        self.assertEqual(invite, None)
        
        friendship = self.session.query(Friendship).filter(Friendship.user_id==user.id).first()

        assert friendship.user_id == user.id
        assert friendship.friend_id == friend.id
        
        friendship.delete()
        friend.delete()
        user.delete()
        
    def test_accept_inexistent_invite(self):
        user = create_logged_user()
        
        self.http_client.fetch(self.get_url('/invite/accept?invite_id=0&auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "Invite not found."}')
        
        user.delete()
        
    def test_accept_duplicated_invite(self):
        user = create_logged_user()
        friend = create_user(last_name = 'test_accept_invite', first_name = 'test_accept_invite',  username = 'test_accept_invite')
        
        friendship = create_friendship(user,friend)
        invite = create_invite(user, friend)
        
        self.http_client.fetch(self.get_url('/invite/accept?invite_id=%s&auth=should-be-user-auth' % invite.id), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, simplejson.dumps({"status": "error", "msg": "You and %s are already friend!" % friend.first_name}))
        
        invite.delete()
        friendship.delete()
        user.delete()
        friend.delete()
    
    def test_get_invites(self):
        user = create_logged_user()
        friend1 = create_user(last_name = 'test_get_invites-1', first_name = 'test_get_invites-1',  username = 'test_get_invites-1')
        friend2 = create_user(last_name = 'test_get_invites-2', first_name = 'test_get_invites-2',  username = 'test_get_invites-2')

        invite1 = create_invite(user, friend1)
        invite2 = create_invite(user, friend2)
        
        self.http_client.fetch(self.get_url('/invite/get.json?auth=should-be-user-auth'), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"invite": [{"username": "test_get_invites-1", "gender": "M", "first_name": "test_get_invites-1", "last_name": "test_get_invites-1"}, {"username": "test_get_invites-2", "gender": "M", "first_name": "test_get_invites-2", "last_name": "test_get_invites-2"}]}')
        
        invite1.delete()
        invite2.delete()
        user.delete()
        friend1.delete()
        friend2.delete()
        
    def test_send_email_invite(self):
        user = create_logged_user()
        
        email = "victor.pantoja@gmail.com"
        
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
        
    def test_send_duplicate_email_invite(self):
        user = create_logged_user()
        
        email = "victor.pantoja@gmail.com"
        
        invite_email = create_invite_email(user=user, email=email)
        
        self.http_client.fetch(self.get_url('/invite/email/send?email=%s&auth=should-be-user-auth' % email), self.stop)
                
        response = self.wait()
        
        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "You have already invited this user. Just relax!"}')

        invite_email.delete()
        user.delete()
    
    def test_accept_email_invite(self):
        pass