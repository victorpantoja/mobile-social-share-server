# coding: utf-8
#!/usr/bin/env python

import beanstalkc, logging
from base64 import b64encode
from mss.core import settings
from mss.utils import Singleton

class BeanstalkHelper(Singleton):

    beanstalk_pool = None
    beanstalk_pool_failed = []
    beanstalk_local = None

    def addHostFailed(self, host):
        for host_failed in self.beanstalk_pool_failed:
            if host_failed == host:
                return
         
        self.beanstalk_pool_failed.append(host)
        
    def addHost(self, host):
        for h in self.beanstalk_pool:
            if h == host:
                return
         
        self.beanstalk_pool.append(host)
    
    def getPool(self):
        
        if not self.beanstalk_pool and self.beanstalk_pool != []:
            self.beanstalk_pool  = []
            for host in settings.BEANSTALK_HOSTS:
                try:
                    self.addHost(beanstalkc.Connection(host=host.split(":")[0], port=int(host.split(":")[1])))
                    logging.info("[BEANSTALK][%s] - conectado com sucesso " % host)
                except beanstalkc.SocketError, se:
                    self.addHostFailed(host)
                    logging.error("[BEANSTALK][%s] - nao foi possivel conectar no momento " % host)
        
        # validando instancias
        for connhost in self.beanstalk_pool:
            try:
                connhost.use("path")
            except beanstalkc.SocketError, se:
                self.beanstalk_pool.remove(connhost)
                self.addHostFailed("%s:%s" % (connhost.host, connhost.port))

        # append failed
        for host in self.beanstalk_pool_failed:
            try:
                self.addHost(beanstalkc.Connection(host=host.split(":")[0], port=int(host.split(":")[1])))
                self.beanstalk_pool_failed.remove(host)
                logging.info("[BEANSTALK][%s] - conectado com sucesso " % host)
            except beanstalkc.SocketError, se:
                logging.error("[BEANSTALK][%s] - nao foi possivel conectar no momento " % host)

        return self.beanstalk_pool

    def getHostLocal(self):
        if self.beanstalk_local:
            try:
                self.beanstalk_local.use("path")
            except beanstalkc.SocketError, se:
                self.beanstalk_local = None
                logging.error("[BEANSTALK][%s] - nao foi possivel conectar no momento LOCAL")
        
        if not self.beanstalk_local:
            host, port = settings.BEANSTALK.split(":")            
            try:
                self.beanstalk_local = beanstalkc.Connection(host=host, port=int(port))
                logging.info("[BEANSTALK][%s] - conectado com sucesso " % host)
            except beanstalkc.SocketError, se:
                logging.error("[BEANSTALK][%s] - nao foi possivel conectar no momento " % host)
        
        return self.beanstalk_local