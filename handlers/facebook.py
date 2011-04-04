# coding: utf-8
#!/usr/bin/env python

from google.appengine.api import memcache
from handlers.base import BaseHandler

class CanvasHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):

        locale = memcache.get("locale")
        content = memcache.get("content")
        
        self.render("facebook/canvas", locale=locale,content=content)
        
