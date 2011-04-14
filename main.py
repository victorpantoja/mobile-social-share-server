# coding: utf-8
#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers.facebook import CanvasHandler
from handlers.context import ContextHandler
from handlers.user import LoginHandler, CreateLoginHandler

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello, webapp World!')

def main():
    routes = [
        (r'/', MainPage),
        (r"/canvas/", CanvasHandler),
        (r"/context", ContextHandler),
        (r"/login", LoginHandler),
        (r"/login/create", CreateLoginHandler)
    ]
    
    application = webapp.WSGIApplication(routes, debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
  main()