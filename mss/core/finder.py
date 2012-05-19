# coding: utf-8
#!/usr/bin/env python
'''
Processo responsavel por gerar a sugestão de amigos
'''

from mss.core import settings
from mss.core.cache.util import get_cache
from mss.core.daemon import Daemon
from mss.models.user import User
from mss.utils.curl import MSSCurl

import logging
import simplejson


class FriendsFinder(Daemon):

    def __init__(self, pidfile):
        return Daemon.__init__(self, pidfile)

    def _get_mss_users(self):
        return User.all()

    def _get_facebook_friends(self, user):

        profile = User.get_profile(user.id)
        friends = []

        if profile:
            token = simplejson.loads(profile.tokens)['facebook']

            token = simplejson.loads(user.get_profile(user.id).tokens)['facebook']

            url = 'https://graph.facebook.com/me/friends?access_token=%s' % token

            response = MSSCurl().get(url=url)
            for user in response['data']:
                #profile = MSSCurl().get(url='https://graph.facebook.com/%s' % user['id'])
                related = self._get_related_friends(user['name'])

                for friend in related:
                    if friend not in friends:
                        friends.append(friend)

        return friends

    def _get_related_friends(self, name):
        return User.search(name.split(' '))

    def _set_cache(self, user, fb_friends):
        cache = get_cache()

        key = 'mss.fb_friends.%s' % user.id

        logging.debug("setting cache for key %s" % key)
        cache.set(key, fb_friends)

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

                    if fb_friends:
                        self._set_cache(user, fb_friends)
                    else:
                        logging.debug("User %s is not connected to Facebook" % user.username)

                    logging.debug("Friends Loaded for user %s!" % user.username)

                logging.debug("Friends Loaded for all users in 2 seconds!")
            except ValueError:
                logging.exception("problems while getting friends!")
