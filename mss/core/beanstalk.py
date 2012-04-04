# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

from mss.core import settings
from mss.core.daemon import Daemon
from mss.utils.curl import MSSCurl

import time, urllib, tinyurl
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

                if self.tube == 'context':
                    self.beanstalkServer.watch("context")

                logging.info("Can be connect with beanstalk")
            except beanstalkc.SocketError, se:
                logging.error("Can not connect to beanstalk on %s:%s" % (self.host, self.port))
                time.sleep(10)

    def send_context_facebook(self, context, token):
        logging.debug("Sending to facebook")

        url = 'https://graph.facebook.com/me/feed?access_token=%s' % token

        message = ''
        if context.get('status'):
            message += context.get('status')
            logging.debug("Context [status]: %s" % context.get('status'))

        if context.get('location'):
            map_url = 'http://maps.google.com/maps?z=18&q=%(location)s(%(text)s)' % {'location': context['location'],'text': context['status']}

            logging.debug("Context [map_url]: %s" % map_url)
            shortened = tinyurl.create_one(map_url)

            message += ' %s' % shortened
            logging.debug("Context [location]: %s" % shortened)

        try:
            return MSSCurl().post(url=url, port=None, postfields={'message': message})
        except Exception, e:
            logging.exception("Can not send post to Facebook: %s" % e)

    def send_context_twitter(self, context, token):
        logging.debug("Sending to Twitter")

        consumer_key = "f1j3JookvHIoe2MBL7HEg"
        consumer_secret = 'kdgLHtmyFh24UVIDIBtFRC9T5LUlRhgtCskIlG1P08'
        access_token_key = '353770828-OeTG1nMJEuMHIKEdVQvrFloXnI9hcUXBROZ8oyiX'
        access_token_secret = 'u30TQhtFmWB9bKgyXrhJ7SNLGuuxO2n3dJfswv66k'

        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

        map_url = 'http://maps.google.com/maps?z=18&q=%(location)s(%(text)s)' % {'location': context['location'],'text': context['status']}

        shortened = tinyurl.create_one(map_url)

        try:
            return api.PostUpdates("%s %s #mss" % (context['status'], shortened))

        except twitter.TwitterError, e:
            logging.exception("Can not send tweet on %s" % e)

    def send_generic_context(self, context, application_name, callback_url):
        logging.debug("Sending to %s via %s" % (application_name, callback_url))

        postfields = urllib.urlencode(context)

        try:
            return MSSCurl().post(url=callback_url, port=None, postfields=postfields)
        except Exception, e:
            logging.exception("Can not send post to %s: %s" % (application_name, e))

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
                    data = simplejson.loads(job.body)
                    logging.debug("job: %s" % data)

                    application = data['application']
                    context = data['context']
                    token = data['token']
                    callback = data['callback_url']

                    if application == 'twitter':
                        result = self.send_context_twitter(context, token)
                        logging.debug("Twitter result: %s" % result)
                    elif application == 'facebook':
                        result = self.send_context_facebook(context, token)
                        logging.debug("Facebook result: %s" % result)
                    elif application == 'gplus':
                        result = self.send_context_gplus(context, token)
                        logging.debug("Google Plus result: %s" % result)
                    else:
                        result = self.send_generic_context(context, application, callback)
                        logging.debug("%s result: %s" % (application, result))

                else:
                    logging.error("DESCARTANDO JOB %s!" % tube)

                logging.debug("job done tube %s" % tube)
                job.delete()
            except beanstalkc.SocketError, se:
                logging.exception("lost connect with beanstalk, trying restablish")
                self.beanstalkServer = None
                self.connect()
