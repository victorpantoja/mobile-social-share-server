# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.invite import Invite
from mss.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import and_

from datetime import datetime
from mss.models.invite_email import InviteEmail
from mss.utils.emailhelper import EmailHelper
from smtplib import SMTPException

import logging, hashlib


class InviteHandler(BaseHandler):
    @authenticated
    def send(self, user, **kw):
        request_handler = kw.get('request_handler')

        username = kw.get('username')

        session = meta.get_session()
        friend = session.query(User).filter(User.username == username).first()

        friendship = session.query(Friendship).filter(Friendship.user_id == user.id).filter(Friendship.friend_id==friend.id).first()

        if friendship:
            return self.render_to_json({"status": "error", "msg": "User is already your friend."}, request_handler)

        if not friend:
            return self.render_to_json({"status": "error", "msg": "User not found."}, request_handler)

        if friend.id == user.id:
            return self.render_to_json({"status": "error", "msg": "You cannot be a friend of yourself!"}, request_handler)

        invite = Invite()
        invite.user_id = user.id
        invite.friend_id = friend.id
        invite.date = datetime.now()

        try:
            invite.save()
        except IntegrityError:
            return self.render_to_json({"status": "error", "msg": "You have already invited this user. Just relax!"}, request_handler)

        return self.render_to_json({"status": "ok", "msg": "Your invite has been sent."}, request_handler)

    @authenticated
    def list(self, user, **kw):
        request_handler = kw.get('request_handler')

        session = meta.get_session()

        invites = session.query(Invite).filter(Invite.user_id == user.id).all()

        invites_lst = [invite.friend.as_dict() for invite in invites]

        return self.render_to_json({'invite': invites_lst}, request_handler)

    @authenticated
    def invitation(self, user, **kw):
        request_handler = kw.get('request_handler')

        session = meta.get_session()

        invites = session.query(Invite).filter(Invite.friend_id == user.id).all()

        invites_lst = [invite.user.as_dict() for invite in invites]

        dict = {'invite': invites_lst}

        return self.render_to_json({'invite': invites_lst}, request_handler)

    @authenticated
    def email(self, user, **kw):
        request_handler = kw.get('request_handler')

        m = hashlib.md5()
        m.update("%s%s" % (kw.get('email'), user.id))

        code = m.hexdigest()

        invite_email = InviteEmail()
        invite_email.user_id = user.id
        invite_email.code = code
        invite_email.date = datetime.now()

        body="""
              Dear: <br />
               <br />
              %s has invited you to join us at Mobile Social Share. <br />
               <br />
              To accept this invite, just click <a href="http://myalbumshare.com:8000/api/invite/email/accept?code=%s">here</a> <br />
               <br />
              Please let us know if you have any questions. <br />
               <br />
              The MSS Team
              """ % (user.first_name, code)

        try:
            mensagem = EmailHelper.mensagem(destinatario=kw.get('email'), corpo=body, strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>', subject="Join us at Mobile Social Share")
            EmailHelper.enviar(mensagem=mensagem, destinatario=kw.get('email'))

        except SMTPException, e:
            logging.exception(str(e))

        try:
            invite_email.save()
        except IntegrityError:
            return self.render_to_json({"status": "error", "msg": "You have already invited this user. Just relax!"}, request_handler)

        return self.render_to_json({"status": "ok", "msg": "Your invite has been sent."}, request_handler)

    @authenticated
    def accept(self, user, **kw):
        request_handler = kw.get('request_handler')

        username = kw.get('username')

        session = meta.get_session()
        friend = session.query(User).filter(User.username == username).first()

        if not friend:
            return self.render_to_json({"status": "error", "msg": "Inexistent user!"}, request_handler)

        invite = session.query(Invite).filter(and_(Invite.user_id == friend.id, Invite.friend_id == user.id)).first()

        if not invite:
            return self.render_to_json({"status": "error", "msg": "Invite not found."}, request_handler)

        if invite.friend_id == user.id:
            friendship = Friendship()
            friendship.user_id = user.id
            friendship.friend_id = friend.id
            friendship.created_dt = datetime.now()

            try:
                friendship.save()
            except IntegrityError:
                return self.render_to_json({"status": "error", "msg": "You and %s are already friend!" % friend.first_name}, request_handler)

            invite.delete()

        return self.render_to_json({"status": "ok", "msg": "User %s is now your friend!" % friend.first_name}, request_handler)

    def accept_email(self, **kw):

        return self.render_to_template("/create_login.html", code=kw.get('code'))
