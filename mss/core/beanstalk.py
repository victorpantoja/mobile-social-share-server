# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

from mss.core import settings
from mss.core.daemon import Daemon
from mss.utils.emailhelper import EmailHelper
from mss.utils.solrhelper import SolrConnection

import os, sys, atexit, getopt, time, shutil
import beanstalkc, pycurl, StringIO, logging
import simplejson

class MssBeanstalk(Daemon):

    beanstalkServer = None
    NGINX_CACHE_ROOT = "/opt/cache/nginx"
    
    def __init__(self, pidfile, host, nginx, tube):
        self.host = host.split(":")[0]
        self.port = host.split(":")[1]
        self.nginx = nginx
        self.tube = tube
        
        return Daemon.__init__(self, pidfile)
        
    '''
        loopback to stablish connect with beanstalk
    '''
    def connect(self):
        while not self.beanstalkServer:
            try:
                self.beanstalkServer = beanstalkc.Connection(host=self.host, port=int(self.port))
                
                if self.tube=='game':
                    self.beanstalkServer.watch("usuario")
                    self.beanstalkServer.watch("path")
                
                logging.info("Can be connect with beanstalk")
            except beanstalkc.SocketError, se:
                logging.error("Can not connect to beanstalk on %s:%s" % (self.host, self.port))
                time.sleep(10)
    
    def clear_usuario(self, uri):
    
        try:
            url = "%s/purge%s" %(self.nginx,uri)
            
            logging.info("cache purge in %s" % url)
            content_io = StringIO.StringIO()
            
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.WRITEFUNCTION, content_io.write)
            curl.perform()
            
            data = content_io.getvalue()
        except Exception, e:
            logging.exception("failed to connect in %s" % url)
        finally:
            curl.close()

            
    def clear_path(self, path):
    
        try:
            full_path = self.NGINX_CACHE_ROOT + "/" + path
            
            for fname in os.listdir(full_path):
                if os.path.isdir(full_path +"/"+ fname):
                    logging.info("cache clear path %s" % full_path +"/"+ fname)
                    shutil.rmtree(full_path +"/"+ fname)
            
        except Exception, e:
            logging.exception("failed to remove dir %s" % full_path)
        
        
    '''
        consummer loop to cache purge
    '''
    def run(self):
    
        logging.info("Cartola Beanstalk Daemon initialized, waiting for job! :D")
        self.connect()
        
        while True:
            
            try:
                job = self.beanstalkServer.reserve()              
                tube = job.stats()['tube']
                
                logging.info("job received tube %s" % tube)
                if tube == 'usuario':
                    self.clear_usuario(uri=job.body)

                elif tube == 'path':
                    self.clear_path(path=job.body)
                    
                else:
                    logging.error("DESCARTANDO JOB %s!" % tube)
                    
                job.delete()
            except beanstalkc.SocketError, se:
                logging.exception("lost connect with beanstalk, trying restablish")
                self.beanstalkServer = None
                self.connect()
    
