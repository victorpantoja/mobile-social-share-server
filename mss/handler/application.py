# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.models.application import Application

import hashlib
import logging


class ApplicationHandler(BaseHandler):

    @authenticated
    def applications(self, **kw):
        request_handler = kw.get('request_handler')

        apps = Application.all()

        app_list = [app.as_dict() for app in apps]

        return self.render_to_json({'applications': app_list}, request_handler)

    def subscribe(self, **kw):
        request_handler = kw.get('request_handler')

        app = Application()
        app.name = request_handler.get_argument('name')
        app.icon = request_handler.get_argument('icon')
        app.callback_url = request_handler.get_argument('callback_url')

        m = hashlib.md5()
        m.update(app.name + app.icon)

        app.token = m.hexdigest()
        try:
            app.save()
        except Exception, e:
            logging.exception(e);
            return self.render_to_json({'status': 'error', 'msg': 'Application already exists.'}, request_handler)

        return self.render_to_json({'status': 'ok', 'msg': app.token}, request_handler)
