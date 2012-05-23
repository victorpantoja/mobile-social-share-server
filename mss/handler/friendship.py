# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache.util import get_cache
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.user import User


class FriendshipsHandler(BaseHandler):
    @authenticated
    def friends(self, user, **kw):
        request_handler = kw.get('request_handler')

        session = meta.get_session()

        friends = session.query(Friendship).filter(Friendship.user_id == user.id).all()

        friends_lst = [friend.friend.as_dict() for friend in friends]

        return self.render_to_json({'friend': friends_lst}, request_handler)

    @authenticated
    def remove(self, user, **kw):
        request_handler = kw.get('request_handler')

        username = kw.get('username')

        session = meta.get_session()
        friend = session.query(User).filter(User.username == username).first()

        if not friend:
            return self.render_to_json({"status": "error", "msg": "Inexistent user!"}, request_handler)

        friend_id = friend.id

        if friend_id == user.id:
            return self.render_to_json({"status": "error", "msg": "Do you hate yourself?!"}, request_handler)

        friendship = session.query(Friendship).filter(Friendship.friend_id == friend_id).filter(User.id==user.id).first()

        if not friendship:
            return self.render_to_json({"status": "error", "msg": "This user are not your friend!"}, request_handler)

        friendship.delete()

        return self.render_to_json({"status": "ok", "msg": "Your friendship has been removed!"}, request_handler)

    @authenticated
    def suggestions(self, user, **kw):
        request_handler = kw.get('request_handler')

        #TODO - passar para o model
        cache = get_cache()
        key = 'mss.friends.%s' % user.id

        friends = cache.get(key)

        #TODO - enviar email se achar?
        if friends:
            return self.render_to_json({"status": "ok", "msg": [friend.as_dict() for friend in friends]}, request_handler)

        return self.render_to_json({"status": "ok", "msg": "There is no suggestion at this time!"}, request_handler)
