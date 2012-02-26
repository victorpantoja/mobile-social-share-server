# coding: utf-8
#!/usr/bin/env python

import tornado
import simplejson

from mss.core.cache.util import get_cache
from mss.models.application import Application
from mss.handler.application import ApplicationHandler, SubscribeHandler
from mss.tests.functional.utils import create_application, create_logged_user

from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase


class ApplicationHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):

        routes = [
            (r"/applications.json", ApplicationHandler),
            (r"/application/subscribe", SubscribeHandler),
        ]

        return tornado.web.Application(routes)

    def test_get_applications(self):

        app1 = create_application(name="facebook", icon="should-be-logo-1", token="should-be-token-1", callback_url="should-be-callback_url-1")
        app2 = create_application(name="twitter", icon="should-be-logo-2", token="should-be-token-2", callback_url="should-be-callback_url-2")

        cache = get_cache()
        cache.set('test_get_applications', 'should-be-user-auth')

        self.http_client.fetch(self.get_url('/applications.json') + '?auth=should-be-user-auth', self.stop)

        response = self.wait()
        self.failIf(response.error)

        try:
            self.assertEquals(response.body, '{"applications": [{"token": "should-be-token-1", "callback_url": "should-be-callback_url-1", "name": "facebook", "icon": "should-be-logo-1"}, {"token": "should-be-token-2", "callback_url": "should-be-callback_url-2", "name": "twitter", "icon": "should-be-logo-2"}]}')
        except Exception, e:
            raise e
        finally:
            app1.delete()
            app2.delete()

    def test_subscribe(self):
        user = create_logged_user(username='test_subscribe')

        app = Application()
        app.name = "test_subscribe"
        app.icon = "should-be-icon"
        app.callback_url = "should-be-callback_url"

        parameters = {'name': app.name, 'icon': app.icon, 'callback_url': app.callback_url}

        request = HTTPRequest(url=self.get_url('/application/subscribe?auth=should-be-user-auth'),method='POST',body=simplejson.dumps(parameters))

        self.http_client.fetch(request, self.stop)

        response = self.wait()
        self.failIf(response.error)

        token = simplejson.loads(response.body)['msg']

        new_app = Application().fetch_by(name='test_subscribe').first()

        assert new_app.name == app.name
        assert new_app.icon == app.icon
        assert new_app.callback_url == app.callback_url
        assert new_app.token == token

        self.http_client.fetch(self.get_url('/applications.json')+'?auth=should-be-user-auth' , self.stop)

        response = self.wait()
        self.failIf(response.error)

        assert response.body == '{"applications": [{"token": "%s", "callback_url": "should-be-callback_url", "name": "test_subscribe", "icon": "should-be-icon"}]}' % token

        new_app.delete()
        user.delete()

    def test_duplicate_subscribe(self):

        user = create_logged_user(username='test_subscribe')

        app = create_application(name="test_subscribe", icon="should-be-icon", token="qqcoisa", callback_url="should-be-callback_url")

        parameters = {'name': app.name, 'icon': app.icon, 'callback_url': app.callback_url}

        request = HTTPRequest(url=self.get_url('/application/subscribe?auth=should-be-user-auth'), method='POST', body=simplejson.dumps(parameters))

        self.http_client.fetch(request, self.stop)

        response = self.wait()
        self.failIf(response.error)

        assert response.body == '{"status": "error", "msg": "Application already exists."}'

        app.delete()
        user.delete()
