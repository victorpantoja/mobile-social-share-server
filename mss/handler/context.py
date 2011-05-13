# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.core.cache import get_cache
import simplejson, twitter
from mss.utils.shorten_url import ShortenURL

class ContextHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)

    def post(self, user, **kw):

        cache = get_cache()
        cache.set("locale",self.get_argument('location'))
        cache.set("content",self.get_argument('text'))
        
        consumer_key = "uXTHwPObQdiDANsQNyN9fA"
        consumer_secret = 'pPHWgoiVF1pKynGTM77CCv1G9CUgtD0BfWkqBYhtA'
        access_token_key = '15043020-6FMt90SSPL5coMpTvuTNIjH8Q2hNumSvSEYh2tqXN'
        access_token_secret = 'cdlZNKne6fSMBVgf80YOiC0J6yin4MtCygHfgkSk'
        
        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
        
        #http://maps.google.com/maps?z=16&q=-22.959506,-43.202353%28qqcoisa%29
        map_url = 'http://maps.google.com/?ie=UTF8&q=%(location)s&ll=%(location)s&z=18' % {'location':self.get_argument('location')}
        
        shortened = ShortenURL().Shorten(map_url)
        
        status = ''
        
        try:
            status = api.PostUpdate("%s %s #mss" % (self.get_argument('text'), shortened))
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'ok', 'msg':status.text}))
            return
        except twitter.TwitterError, e:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':e.message}))            


