# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.models.user import User

from datetime import datetime
from random import choice

import string
import simplejson

class LoginHandler(BaseHandler):
    pass

class RescueLoginHandler(BaseHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        
        user = User()
        user.first_name = "teste"
        user.last_name = "teste"
        
        username = self.request.GET[u'username']
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({'status':'ok', 'msg':'Password re-created! Verify you email account'}))    
        
class CreateLoginHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
                
        user = User()
        user.username = self.get_argument('username')
        
        user.first_name = self.get_argument('firstName')
        user.last_name = self.get_argument('lastName')
        user.password = self.create_random_passord()
        user.created = datetime.now()
        user.last_login = datetime.now()

        try:
            user.save()
        except:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Username already exists.'}))
            return
        
#        mail.send_mail(sender="Example.com Support <victor.pantoja@gmail.com>",
#              to="%s %s <%s>" % (user.firstName, user.lastName, user.username),
#              subject="Your account has been created",
#              body="""
#                    Dear User:
#                    
#                    Your has been created. You can now start using Mobile Social Share.
#                    
#                    You temporary password is %s. We strongly recommend you change as soon as possible.
#                    
#                    Please let us know if you have any questions.
#                    
#                    The MSS Team
#                    """ % user.password)
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':'Account Created! Verify you email account'}))
        return
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        
