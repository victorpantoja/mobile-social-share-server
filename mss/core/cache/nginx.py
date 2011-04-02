# coding: utf-8
#!/usr/bin/env python

import beanstalkc, logging
from base64 import b64encode
from mss.core import settings
from mss.utils.beanstalkhelper import BeanstalkHelper

class MssCacheNginx():

    @staticmethod
    def expire_path(path):
        beanstalk_pool = BeanstalkHelper().getPool()
        
        for beanstalk in beanstalk_pool:
            beanstalk.use("path")
            beanstalk.put(path)
            logging.debug("[BEANSTALK][%s][PUT] - expire_path(%s)" % (beanstalk.host,path))    
                
    
    @staticmethod
    def expire_home(time=None, time_id=None):
        
        beanstalk_pool = BeanstalkHelper().getPool()
        
        for beanstalk in beanstalk_pool:
            beanstalk.use("usuario")
            uri = "/home/" + b64encode(str(time_id if time_id else time.id))
            beanstalk.put(uri)
            
            logging.debug("[BEANSTALK][%s][PUT] - expire_home(%s)" % (beanstalk.host,uri))        
