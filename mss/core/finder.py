# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por consumir a fila do beanstalkd, e expirar o cache nos nginxs
'''

from mss.core import settings
from mss.core.daemon import Daemon
from mss.models.user import User
from mss.utils import get_cache

import logging


class FriendsFinder(Daemon):

    def __init__(self, pidfile):
        return Daemon.__init__(self, pidfile)
        
    def _get_mss_users(self):
        return User.all()
        
    def _get_facebook_friends(self, user):
        
        return []
        
    def _set_cache(self, user, fb_friends):
        cache = get_cache()
        
        key = 'mss.fb_friends.%s' % user.id
        
        logging.debug("setting cache for key %" % key)
        result = cache.set(md5key, fb_friends)

    '''
        consummer loop to finds friends
    '''
    def run(self):

        logging.info("MSS Friends Finder Daemon initialized!")

        while True:
            try:
                logging.debug("Gonna find some guys...")
                                
                users = self._get_mss_users()
                
                for user in users:
                    logging.debug("Gonna load friends for user %s!" % user.username)
                    fb_friends = self._get_facebook_friends(user)
                    self._set_cache(user, fb_friends)
                
                    logging.debug("Friends Loaded for user %s!" % user.username)
                    
                logging.debug("Friends Loaded for all users in 2 seconds!")    
            except ValueError:
                logging.exception("problems while getting friends!")
