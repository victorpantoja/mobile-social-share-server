# coding: utf-8
#!/usr/bin/env python

from google.appengine.api import users, mail
from google.appengine.ext import webapp, db
from models.user import User

from datetime import datetime
from random import choice

import string
import simplejson

class LoginHandler(webapp.RequestHandler):
    pass

class RescueLoginHandler(webapp.RequestHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        
        username = self.request.GET[u'username']
        
        user = User.get(None)
        
        mail.send_mail(sender="Example.com Support <victor.pantoja@gmail.com>",
              to="%s %s <%s>" % (user.firstName, user.lastName, user.username),
              subject="Your account has been created",
              body="""
                    Dear User:
                    
                    Your password has been changed.
                    
                    You temporary password is %s. We strongly recommend you change as soon as possible.
                    
                    Please let us know if you have any questions.
                    
                    The MSS Team
                    """ % user.password)
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({'status':'ok', 'msg':'Password re-created! Verify you email account'}))    
        
class CreateLoginHandler(webapp.RequestHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
        
        user_str = ""
        
        user = User()
        user.username = self.request.GET[u'username']
        
        _users = db.GqlQuery("SELECT * FROM User where username = '"+user.username+"'")
         
        if _users.count() > 0:
           self.response.headers['Content-Type'] = 'application/json'
           self.response.out.write(simplejson.dumps({'status':'error', 'msg':'Username already exists.'}))
           return
        
        user.firstName = self.request.GET[u'firstName']
        user.lastName = self.request.GET[u'lastName']
        user.password = self.create_random_passord()
        user.created = datetime.now()
        
        user.save()
        
        mail.send_mail(sender="Example.com Support <victor.pantoja@gmail.com>",
              to="%s %s <%s>" % (user.firstName, user.lastName, user.username),
              subject="Your account has been created",
              body="""
                    Dear User:
                    
                    Your has been created. You can now start using Mobile Social Share.
                    
                    You temporary password is %s. We strongly recommend you change as soon as possible.
                    
                    Please let us know if you have any questions.
                    
                    The MSS Team
                    """ % user.password)
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({'status':'ok', 'msg':'Account Created! Verify you email account'}))
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        
