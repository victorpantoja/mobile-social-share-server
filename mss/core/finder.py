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
import twitter


class FriendsFinder(Daemon):

    def __init__(self, pidfile):
        return Daemon.__init__(self, pidfile)

    def _get_mss_users(self):
        return User.all()

    def _get_facebook_friends(self, user):

        fb_friends = []
        profile = User.get_profile(user.id)

        if profile:
            token = simplejson.loads(profile.tokens)['facebook']

            #TODO - resolver problema de cache do UserProfile

            url = 'https://graph.facebook.com/me/friends?access_token=%s' % token

            response = MSSCurl().get(url=url)
            for user in response['data']:
                #profile = MSSCurl().get(url='https://graph.facebook.com/%s' % user['id'])
                fb_friends.extend(self._get_related_friends(user['name']))

        return fb_friends

    def _get_twitter_friends(self, user):

        tw_friends = []
        profile = User.get_profile(user.id)

        if profile:
            token = simplejson.loads(profile.tokens)['twitter']

            consumer_key = "f1j3JookvHIoe2MBL7HEg"
            consumer_secret = 'kdgLHtmyFh24UVIDIBtFRC9T5LUlRhgtCskIlG1P08'
            access_token_key = '353770828-OeTG1nMJEuMHIKEdVQvrFloXnI9hcUXBROZ8oyiX'
            access_token_secret = 'u30TQhtFmWB9bKgyXrhJ7SNLGuuxO2n3dJfswv66k'

            api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

            try:
                users = api.GetFriends('sauloaride')
            except twitter.TwitterError, e:
                logging.exception("Can not get twitter friends on %s" % e)

            for user in users:
                tw_friends.extend(self._get_related_friends(user.name))

        return tw_friends

    def _get_related_friends(self, name):
        return User.search(name.split(' '))

    def _set_cache(self, user, friends):
        cache = get_cache()

        key = 'mss.friends.%s' % user.id

        logging.debug("setting cache for key %s" % key)
        cache.set(key, friends)

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

                    tw_friends = self._get_twitter_friends(user)
                    fb_friends = self._get_facebook_friends(user)

                    friends = []

                    for friend in tw_friends:
                        if friend not in friends:
                            friends.append(friend)

                    for friend in fb_friends:
                        if friend not in friends:
                            friends.append(friend)

                    self._set_cache(user, friends)

                    logging.debug("Friends Loaded for user %s!" % user.username)

                logging.debug("Friends Loaded for all users in 2 seconds!")
            except ValueError:
                logging.exception("problems while getting friends!")
