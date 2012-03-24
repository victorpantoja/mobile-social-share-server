# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.utils.curl import MSSCurl

import urlparse


class AuthorizationHandler(BaseHandler):

    def get(self, **kw):

        code = self.get_argument('code')

        client_id = '113400205406273'
        secret = '26cfa7320bf675ea1288522178a45bb5'
        redirect_uri = 'http://myalbumshare.com:9080/auth'

        url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (client_id, redirect_uri, secret, code)

        data = MSSCurl().get(str(url), 'plain')

        response = urlparse.parse_qs(data)

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(response))

        return
