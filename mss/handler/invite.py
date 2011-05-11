# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.user import User
from sqlalchemy.exceptions import IntegrityError

from datetime import datetime
import simplejson


class SendInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return
        
class GetInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return
    
class SendEmailInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return
    
class AcceptInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return
    
class AcceptEmailInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return