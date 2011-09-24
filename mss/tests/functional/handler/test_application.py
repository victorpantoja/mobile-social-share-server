# coding: utf-8
#!/usr/bin/env python

import tornado

from mss.core.cache.util import get_cache
from mss.handler.application import ApplicationHandler
from mss.models.application import Application
from tornado.testing import AsyncHTTPTestCase
from mss.core import meta
from mss.tests.functional.utils import create_application


class NetworkHandlerTestCase(AsyncHTTPTestCase):
    
    def get_app(self):
        
        routes = [
            (r"/applications.json", ApplicationHandler),
        ]
        
        return tornado.web.Application(routes)
    
    
    def test_get_applications(self):
        
        app1 = create_application(name="facebook",icon="should-be-logo-1",token="should-be-token-1",callback_url="should-be-callback_url-1")
        app2 = create_application(name="twitter",icon="should-be-logo-2",token="should-be-token-2",callback_url="should-be-callback_url-2")
        
        cache = get_cache()
        cache.set('test_get_applications', 'should-be-user-auth')
        
        self.http_client.fetch(self.get_url('/applications.json')+'?auth=test_get_applications' , self.stop)
                
        response = self.wait()
        self.failIf(response.error)
                
        try:
            self.assertEquals(response.body,'{"applications": [{"token": "should-be-token-1", "callback_url": "should-be-callback_url-1", "name": "facebook", "icon": "should-be-logo-1"}, {"token": "should-be-token-2", "callback_url": "should-be-callback_url-2", "name": "twitter", "icon": "should-be-logo-2"}]}')
        except Exception, e:
            raise e
        finally:
            app1.delete()
            app2.delete()
        
