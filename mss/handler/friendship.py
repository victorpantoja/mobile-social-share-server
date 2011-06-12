# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.user import User

import simplejson
        
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
        
        username = self.get_argument('username')
        
        session = meta.get_session()
        friend = session.query(User).filter(User.username==username).first()
        
        if not friend:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "Inexistent user!"}))
            return  
                   
        friend_id = friend.id
        
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