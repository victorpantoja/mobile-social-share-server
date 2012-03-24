# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler


class StatusHandler(BaseHandler):
    def status(self, **kw):
        return self.render_to_template("/status.html")