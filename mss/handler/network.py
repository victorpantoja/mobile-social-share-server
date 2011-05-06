# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
import simplejson
from mss.core import meta
from mss.models.network import Network

class NetworkHandler(BaseHandler):

    @authenticated    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
        
        session = meta.get_session()
        
        nets = session.query(Network).all()
        
        net_list = [net.as_dict() for net in nets]
        
        dict = {'networks':net_list}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return