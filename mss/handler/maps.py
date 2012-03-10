# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.utils.curl import MSSCurl
import simplejson


class MapsHandler(BaseHandler):

    def get(self, **kw):

        origin = str(self.get_argument('origin')) #-23.0028,-43.3493
        destination = str(self.get_argument('destination')) #-22.9989,-43.3600

        data = MSSCurl().get("http://maps.google.com/maps/api/directions/json?origin=%s&destination=%s&sensor=true" % (origin, destination) )

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(data))

        return
