# coding: utf-8
#!/usr/bin/env python

from mss.core.cache import get_cache
from mss.handler.context import ContextHandler
from tornado.testing import AsyncHTTPTestCase
import tornado

class ContextHandlerTestCase(AsyncHTTPTestCase):
    
    def get_app(self):
        
        routes = [
            (r"/context", ContextHandler)
        ]
        
        return tornado.web.Application(routes)
    
    
    def test_send_context(self):
        
        cache = get_cache()
        cache.set('should-be-key', 'should-be-user-auth')
        
        self.http_client.fetch(self.get_url('/context')+'?location=-22.95835442222223,-43.196200622222214&text=qqcoisa&auth=should-be-key' , self.stop)
                
        response = self.wait()
        self.failIf(response.error)
        
        cache = get_cache()
        locale = cache.get("locale")
        content = cache.get("content")
        
        assert locale == '-22.95835442222223,-43.196200622222214'
        assert content == 'qqcoisa'