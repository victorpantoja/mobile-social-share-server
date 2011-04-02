# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.core.cache import get_cache

class ContextHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):

        cache = get_cache()
        cache.set("locale","-22.95799, -43.19406")
        cache.set("content","<b>Victor Pantoja</b><br />Hey! I'm Here!")

        return "OK"
