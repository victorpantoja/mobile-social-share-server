# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.core.cache import get_cache

class CanvasHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):

        cache = get_cache()
        locale = cache.get("locale")
        content = cache.get("content")
        
        self.render_template("facebook/canvas.html",locale=locale, content=content)
