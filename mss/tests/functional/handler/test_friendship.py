# coding: utf-8
#!/usr/bin/env python

from mss.core.meta import get_session
from mss.handler.friendship import GetFriendshipsHandler
from mss.handler.friendship import RemoveFriendshipsHandler
from mss.models.friendship import Friendship
from mss.tests.functional.utils import create_logged_user
from mss.tests.functional.utils import create_user
from mss.tests.functional.utils import create_friendship
from tornado.testing import AsyncHTTPTestCase

import tornado


class FriendshipHandlerTestCase(AsyncHTTPTestCase):

    session = get_session()

    def get_app(self):

        routes = [
            (r"/friendship/get.json", GetFriendshipsHandler),
            (r"/friendship/remove", RemoveFriendshipsHandler)
        ]

        return tornado.web.Application(routes)

    def test_get_friendship(self):
        user = create_logged_user()
        user2 = create_user(last_name='test_get_friendship-2', first_name='test_get_friendship-2',  username='test_get_friendship-2')
        user3 = create_user(last_name='test_get_friendship-3', first_name='test_get_friendship-3',  username='test_get_friendship-3')

        friendship = create_friendship(user, user2)
        friendship2 = create_friendship(user, user3)

        self.http_client.fetch(self.get_url('/friendship/get.json?auth=should-be-user-auth'), self.stop)

        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"friend": [{"username": "test_get_friendship-2", "first_name": "test_get_friendship-2", "last_name": "test_get_friendship-2", "gender": "M", "is_active": true, "is_superuser": false, "is_staff": false, "email": "should-be-email"}, {"username": "test_get_friendship-3", "first_name": "test_get_friendship-3", "last_name": "test_get_friendship-3", "gender": "M", "is_active": true, "is_superuser": false, "is_staff": false, "email": "should-be-email"}]}')

        friendship.delete()
        friendship2.delete()
        user3.delete()
        user2.delete()
        user.delete()

    def test_remove_friendship(self):
        user = create_logged_user()
        user2 = create_user(last_name='test_remove_friendship-2', first_name='test_remove_friendship-2',  username='test_remove_friendship-2')

        create_friendship(user, user2)

        self.http_client.fetch(self.get_url('/friendship/remove?username=%s&auth=should-be-user-auth' % user2.username), self.stop)

        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "ok", "msg": "Your friendship has been removed!"}')
        friendship_db = self.session.query(Friendship).filter(Friendship.user_id == user.id).first()

        self.assertEqual(friendship_db, None)

        user.delete()
        user2.delete()

    def test_remove_myself_friendship(self):

        user = create_logged_user()

        self.http_client.fetch(self.get_url('/friendship/remove?username=%s&auth=should-be-user-auth' % user.username), self.stop)

        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "Do you hate yourself?!"}')

        user.delete()

    def test_remove_inexistent_friendship(self):
        user = create_logged_user(username='remove_inexistent_friendship-1')
        user2 = create_user(last_name='remove_inexistent_friendship-2', first_name='remove_inexistent_friendship-2',  username='remove_inexistent_friendship-2')

        self.http_client.fetch(self.get_url('/friendship/remove?username=%s&auth=should-be-user-auth' % user2.username), self.stop)

        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "This user are not your friend!"}')

        user.delete()
        user2.delete()

    def test_remove_inexistent_friendship_with_inexistent_user(self):
        user = create_logged_user()

        self.http_client.fetch(self.get_url('/friendship/remove?username=0&auth=should-be-user-auth'), self.stop)

        response = self.wait()

        self.failIf(response.error)
        self.assertEqual(response.body, '{"status": "error", "msg": "Inexistent user!"}')

        user.delete()
