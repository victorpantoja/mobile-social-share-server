import os

from google.appengine.ext.webapp import template, RequestHandler

class BaseHandler(RequestHandler):

    def render(self, name, **data):
        """Render a template"""
        if not data:
            data = {}

        self.response.out.write(template.render(
            os.path.join(
                os.path.dirname(__file__), '../templates', name + '.html'),
            data))