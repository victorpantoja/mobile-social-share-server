# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler

class CanvasHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
        
        self.render_template("facebook/canvas.html")
