# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import get_cache
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.user import User
from sqlalchemy.exceptions import IntegrityError

from datetime import datetime
import simplejson

class CreateFriendshipHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):
                
        friend_id = int(self.get_argument('friend_id'))
        
        if friend_id == user.id:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "You cannot be a friend of yourself!"})) 
            return
        
        friend = User.get(id=friend_id)
        
        if not friend:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "User not found."})) 
            return

        friendship = Friendship()
        
        friendship.user_id = user.id
        friendship.friend_id = friend.id
        friendship.created_dt = datetime.now()
        
        try:  
            friendship.save()
        except IntegrityError:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "You and %s are already friend!" % friend.first_name}))
            return
            
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "User %s is now your friend!" % friend.first_name}))  
        return
        
class GetFriendshipsHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)

    def post(self, user, **kw):
        session = meta.get_session()

        friends = session.query(Friendship).filter(Friendship.user_id==user.id).all()
                
        friends_lst = [friend.friend.as_dict() for friend in friends]
        
        dict = {'friend':friends_lst}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return
    
class RemoveFriendshipsHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)

    def post(self, user, **kw):
        session = meta.get_session()
        
        friend_id = int(self.get_argument('friend_id'))
        
        if friend_id == user.id:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "Do you hate yourself?!"}))
            return
        
        friendship = session.query(Friendship).filter(Friendship.friend_id==friend_id).filter(User.id==user.id).first()
                
        if not friendship:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "This user are not your friend!"}))
            return
        
        friendship.delete()

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "Your friendship has been removed!"}))
        return