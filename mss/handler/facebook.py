# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.utils.curl import MSSCurl

import urlparse


class AuthorizationHandler(BaseHandler):

    def auth(self, **kw):
        request_handler = kw.get('request_handler')

        code = kw.get('code')

        client_id = '113400205406273'
        secret = '26cfa7320bf675ea1288522178a45bb5'
        redirect_uri = 'http://myalbumshare.com:9080/auth'

        url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (client_id, redirect_uri, secret, code)

        data = MSSCurl().get(str(url), 'plain')

        response = urlparse.parse_qs(data)

        return self.render_to_json(response, request_handler)

        return
