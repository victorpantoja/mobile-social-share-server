# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.core.cache import get_cache

class ContextHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):

        cache = get_cache()
        cache.set("locale",self.get_argument('location'))
        cache.set("content",self.get_argument('text'))

        self.write("ok")
