# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.utils.curl import MSSCurl
import simplejson


class MapsHandler(BaseHandler):

    @authenticated
    def get(self, **kw):

        origin = str(self.get_argument('origin')) #-23.0028,-43.3493
        destination = str(self.get_argument('destination')) #-22.9989,-43.3600
        filters = str(self.get_argument('filters')).split(',')

        self.data = MSSCurl().get("http://maps.google.com/maps/api/directions/json?origin=%s&destination=%s&sensor=true" % (origin, destination) )
                
        resp = {}
        
        for filter in filters:
            keys = filter.split('/')
            resp[keys[len(keys)-1]] = self._get_value(filter)

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(resp))

        return

    def _get_value(self, filter):
        value = self.data['routes'][0]
                
        for key in filter.split('/'):
            if type(value) == list:
                value = value[0].get(key)
            else:
                value = value.get(key)
        
        return value