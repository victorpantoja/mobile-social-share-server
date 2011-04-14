# coding: utf-8
#!/usr/bin/env python

from google.appengine.api import users, mail
from google.appengine.ext import webapp
from models.user import User

from datetime import datetime
from random import choice

import string

class LoginHandler(webapp.RequestHandler):
    pass

class CreateLoginHandler(webapp.RequestHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
        
        user = User()
        user.username = users.User("victor.pantoja@gmail.com")
        user.password = self.create_random_passord()
        user.created = datetime.now()
        
        user.save()
        
        mail.send_mail(sender="Example.com Support <victor.pantoja@gmail.com>",
              to="Victor Pantoja <victor.pantoja@gmail.com>",
              subject="Your account has been created",
              body="""
                    Dear User:
                    
                    Your has been created. You can now start using Mobile Social Share.
                    
                    You temporary password is %s. We strongly recommend you change as soon as possible.
                    
                    Please let us know if you have any questions.
                    
                    The MSS Team
                    """ % user.password)
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        