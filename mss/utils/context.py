# coding: utf-8
#!/usr/bin/env python

import logging, simplejson

from mss.utils import Singleton
from mss.utils.beanstalkhelper import BeanstalkHelper

class ContextQueue(Singleton):
    
    def add(self, context):
        try:
            queue = BeanstalkHelper().getHostLocal()
                        
            data = simplejson.dumps(context)
            
            logging.debug("[ContextQueue] message=%s" % data)
            
            queue.use("context")
            logging.debug("[ContextQueue] use=context OK")
            queue.put(data)

            logging.debug("[ContextQueue] - PUT OK %s" % data)
        except Exception, e:
            logging.exception("[ContextQueue] Nao foi possivel realizar o put agora")