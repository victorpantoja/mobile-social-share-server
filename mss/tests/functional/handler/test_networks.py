# coding: utf-8
#!/usr/bin/env python

import tornado

from mss.core.cache.util import get_cache
from mss.handler.network import NetworkHandler
from mss.models.network import Network
from tornado.testing import AsyncHTTPTestCase
from mss.core import meta


class NetworkHandlerTestCase(AsyncHTTPTestCase):
    
    def get_app(self):
        
        routes = [
            (r"/networks.json", NetworkHandler),
        ]
        
        return tornado.web.Application(routes)
    
    
    def test_get_networks(self):
        
        net1 = Network()
        net1.name = "facebook"
        net1.icon = "should-be-logo-1"
        net1.save()
        
        net2 = Network()
        net2.name = "twitter"
        net2.icon = "should-be-logo-2"
        net2.save()
        
        cache = get_cache()
        cache.set('test_get_networks', 'should-be-user-auth')
        
        self.http_client.fetch(self.get_url('/networks.json')+'?auth=test_get_networks' , self.stop)
                
        response = self.wait()
        self.failIf(response.error)
        
        try:
            self.assertEquals(response.body,'{"networks": [{"name": "facebook", "icon": "should-be-logo-1"}, {"name": "twitter", "icon": "should-be-logo-2"}]}')
        except Exception, e:
            raise e
        finally:
            session = meta.get_session()

            net1_db = session.query(Network).filter(Network.name=='facebook').first()
            net1_db.delete()
            
            net2_db = session.query(Network).filter(Network.name=='twitter').first()
            net2_db.delete()
        
