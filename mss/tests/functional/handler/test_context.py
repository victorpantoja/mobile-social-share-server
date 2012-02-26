# coding: utf-8
#!/usr/bin/env python

from mss.models.context import Context
from mss.handler.context import ContextHandler
from mss.models.context_application import ContextApplication
from mss.tests.functional.utils import create_application, create_logged_user

from tornado.testing import AsyncHTTPTestCase
from tornado.httpclient import HTTPRequest

import tornado
import simplejson
import string
import random


class ContextHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):

        routes = [
            (r"/context", ContextHandler)
        ]

        return tornado.web.Application(routes)

    def test_send_context(self):

        user = create_logged_user(username='test_send_context')

        app1 = create_application(name="twitter")

        text = ''.join([random.choice(string.letters) for x in xrange(5)])

        parameters = {'application': [app1.name], 'context': {'location': '-22.95835442222223,-43.196200622222214','status': text}}

        request = HTTPRequest(url=self.get_url('/context?auth=should-be-user-auth'), method='POST',body=simplejson.dumps(parameters))

        self.http_client.fetch(request, self.stop)

        response = self.wait()
        self.failIf(response.error)

        assert simplejson.loads(response.body)['status'] == 'ok'

        context1 = Context().fetch_by(context=text).first()
        context2 = Context().fetch_by(context='-22.95835442222223,-43.196200622222214').first()

        context_applicaton1 = ContextApplication.fetch_by(context_id=context1.id).first()
        context_applicaton2 = ContextApplication.fetch_by(context_id=context2.id).first()

        assert context1.context == text
        assert context2.context == '-22.95835442222223,-43.196200622222214'
        assert context_applicaton1.context_id == context1.id
        assert context_applicaton2.context_id == context2.id

        context_applicaton1.delete()
        context_applicaton2.delete()

        context1.delete()
        context2.delete()

        user.delete()

        app1.delete()
