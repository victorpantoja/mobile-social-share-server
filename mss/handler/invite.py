# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.invite import Invite
from mss.models.user import User
from sqlalchemy.exceptions import IntegrityError

from datetime import datetime
import hashlib, simplejson
from mss.models import invite_email
from mss.models.invite_email import InviteEmail

class SendInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        invite = Invite()
        invite.user_id = user.id
        invite.friend_id = self.get_argument('friend_id')
        invite.date = datetime.now()
        
        try:
            invite.save()
        except IntegrityError:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "You have already invited this user. Just relax!"}))
            return

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "Your invite has been sent."}))  
        return
        
class GetInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):
        session = meta.get_session()
        
        invites = session.query(Invite).filter(Invite.user_id==user.id).all()
                
        invites_lst = [invite.friend.as_dict() for invite in invites]
        
        dict = {'invite':invites_lst}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return
    
class SendEmailInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):
        
        m = hashlib.md5()
        m.update("%s%s" % (self.get_argument('email'),user.id))
        
        code = m.hexdigest()
        
        invite_email = InviteEmail()
        invite_email.user_id = user.id
        invite_email.code = code
        invite_email.date = datetime.now()
        
        try:
            invite_email.save()
        except IntegrityError:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "You have already invited this user. Just relax!"}))
            return

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "Your invite has been sent."}))  
        return
    
class AcceptInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):
        
        invite_id = int(self.get_argument('invite_id'))
        
        invite = Invite.get(id=invite_id)
        
        if not invite:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "Invite not found."}))  
            return 
        
        if invite.user_id == user.id:
            friendship = Friendship()
            friendship.user_id = user.id
            friendship.friend_id = invite.friend_id
            friendship.created_dt = datetime.now()
            friendship.save()
            
            invite.delete()

        friend = User.get(id=invite.friend_id)

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "User %s is now your friend!" % friend.first_name}))  
        return
    
class AcceptEmailInviteHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": ""}))  
        return