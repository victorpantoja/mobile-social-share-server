# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

from mss.core import settings
from mss.core.daemon import Daemon
from mss.utils.shorten_url import ShortenURL
from mss.utils.curl import MSSCurl

import time, urllib
import beanstalkc, logging
import simplejson, twitter

class MSSBeanstalk(Daemon):

    beanstalkServer = None
    
    def __init__(self, pidfile, host, tube):
        self.host = host.split(":")[0]
        self.port = host.split(":")[1]
        self.tube = tube
        
        return Daemon.__init__(self, pidfile)
        
    '''
        loopback to stablish connect with beanstalk
    '''
    def connect(self):
        while not self.beanstalkServer:
            try:
                self.beanstalkServer = beanstalkc.Connection(host=self.host, port=int(self.port))
                
                if self.tube=='context':
                    self.beanstalkServer.watch("context")
                
                logging.info("Can be connect with beanstalk")
            except beanstalkc.SocketError, se:
                logging.error("Can not connect to beanstalk on %s:%s" % (self.host, self.port))
                time.sleep(10)

            
    def send_context(self, job):
        
        data = simplejson.loads(job)
        
        result = self.send_context_facebook(data['context'])
        twitter = self.send_context_twitter(data['context'])
        
    
    def send_context_facebook(self,context):
        url = 'https://graph.facebook.com/me/feed?access_token=AAABnIwr18EEBAIZCZCVWvEr5jnhKtZCXEjidzisJ62TKhR2ggKvXcgjUwaYvuwv1UjPqmQZCLySfxxv5YCNZAiSZCHHig2knYMF5g2hB7O8hrrtgVOIn7r'

        postfields = urllib.urlencode({'message':context['data']})

        try:
            return MSSCurl.post(url,postfields)
        except Exception, e:
            logging.exception("Can not send tweet on %s" % e)
            
    def send_context_twitter(self,context):
        consumer_key = "f1j3JookvHIoe2MBL7HEg"
        consumer_secret = 'kdgLHtmyFh24UVIDIBtFRC9T5LUlRhgtCskIlG1P08'
        access_token_key = '353770828-OeTG1nMJEuMHIKEdVQvrFloXnI9hcUXBROZ8oyiX'
        access_token_secret = 'u30TQhtFmWB9bKgyXrhJ7SNLGuuxO2n3dJfswv66k'
        
        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
        
        map_url = 'http://maps.google.com/maps?z=18&q=%(location)s(%(text)s)' % {'location':context['location'],'text':context['status']}
        
        shortened = ShortenURL().Shorten(map_url)
                
        try:
            logging.debug("Sending tweet")
            return api.PostUpdate("%s %s #mss" % (context['status'], shortened))

        except twitter.TwitterError, e:
            logging.exception("Can not send tweet on %s" % e)
    '''
        consummer loop to cache purge
    '''
    def run(self):
    
        logging.info("MSS Beanstalk Daemon initialized, waiting for job! :D")
        self.connect()
        
        while True:
            
            try:
                job = self.beanstalkServer.reserve()              
                tube = job.stats()['tube']
                
                logging.info("job received tube %s" % tube)
                if tube == 'context':
                    self.send_context(job.body)
                    
                else:
                    logging.error("DESCARTANDO JOB %s!" % tube)
                    
                job.delete()
            except beanstalkc.SocketError, se:
                logging.exception("lost connect with beanstalk, trying restablish")
                self.beanstalkServer = None
                self.connect()
    
