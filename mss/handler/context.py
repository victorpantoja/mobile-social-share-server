# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.core.cache import get_cache
import simplejson

class ContextHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)

    def post(self, user, **kw):

        cache = get_cache()
        cache.set("locale",self.get_argument('location'))
        cache.set("content",self.get_argument('text'))

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':'Informations Sent.'}))
        return 
