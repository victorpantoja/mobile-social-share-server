# coding: utf-8
#!/usr/bin/env python

from google.appengine.api import memcache
from google.appengine.ext import webapp

class ContextHandler(webapp.RequestHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
        memcache.set("locale",self.request.GET[u'location'])
        memcache.set("content",self.request.GET[u'text'])

