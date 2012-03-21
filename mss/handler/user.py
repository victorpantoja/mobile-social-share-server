# coding: utf-8
#!/usr/bin/env python

from datetime import datetime
from mss.core import meta
from mss.core.cache import get_cache
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.invite import Invite
from mss.models.invite_email import InviteEmail
from mss.models.user import User
from mss.utils import create_random_string
from mss.utils.emailhelper import EmailHelper
from random import getrandbits
from smtplib import SMTPException

import logging
import hashlib
import string
import simplejson


class UserHandler(BaseHandler):

    def create(self, **kw):

        request_handler = kw.get('request_handler')

        user = User()
        user.username = kw.get('username')
        user.email = kw.get('email')
        user.is_staff = True
        user.is_superuser = False
        user.is_active = True

        try:
            EmailHelper.validateEmail(user.email)
        except Exception, e:
            logging.exception(e);
            return self.render_to_json({'status': 'error', 'msg': 'Invalid email.'}, request_handler)

        user.first_name = kw.get('firstName')
        user.last_name = kw.get('lastName')
        user.gender = kw.get('gender')

        password = create_random_string()

        m = hashlib.sha1()
        m.update(password)

        user.password = 'sha1$$' + m.hexdigest()
        user.created = datetime.now()
        user.last_login = datetime.now()

        body = """
              Dear %s: <br />
               <br />
              Your account has been created. You can now start using Mobile Social Share. <br />
               <br />
              You temporary password is %s. We strongly recommend you change as soon as possible. <br />
               <br />
              Please let us know if you have any questions. <br />
               <br />
              The MSS Team
              """ % (user.first_name, password)

        try:
            user.save()
        except Exception, e:
            logging.exception(e)
            return self.render_to_json({'status': 'error', 'msg': 'Username already exists.'}, request_handler)

        try:
            mensagem = EmailHelper.mensagem(destinatario=user.email, corpo=body, strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>', subject="Your account has been created")
            EmailHelper.enviar(mensagem=mensagem, destinatario=user.email)

        except SMTPException, e:
            logging.exception(str(e))

        code = kw.get("code", "")
        if code != "":
            session = meta.get_session()
            invite_email = session.query(InviteEmail).filter(InviteEmail.code==code).first()

            if invite_email:
                friendship = Friendship()
                friendship.user_id = invite_email.user_id
                friendship.friend_id = user.id
                friendship.created_dt = datetime.now()
                friendship.save()

                invite_email.delete()

        return self.render_to_json({'status': 'ok', 'msg': 'Account Created! Verify you email account'}, request_handler)

    def login(self, **kw):

        request_handler = kw.get('request_handler')

        username = kw.get('username')
        password = kw.get('password')

        session = meta.get_session()
        user = session.query(User).filter(User.username==username).first()

        m = hashlib.sha1()
        m.update(password)

        password = 'sha1$$' + m.hexdigest()

        if user and (user.password == password):

            auth = hashlib.md5()
            auth.update('%s' % getrandbits(32))

            cache = get_cache()
            cache.set(auth.hexdigest(), '%s' % user.username)

            invites = session.query(Invite).filter(Invite.friend_id==user.id).all()
            invites_lst = [invite.user.as_dict() for invite in invites] 
        else:
            return self.render_to_json({'status': 'error', 'msg': 'Wrong username or password.'}, request_handler)

        return self.render_to_json({'status': 'ok', 'msg': auth.hexdigest(),'invites': invites_lst}, request_handler)

    @authenticated
    def search(self, user, **kw):

        request_handler = kw.get('request_handler')

        username = kw.get('username')

        #TODO - Escape
        session = meta.get_session()
        users = session.query(User).filter(User.username.like("%" + username + "%")).order_by(User.first_name).all()

        users_lst = [user.as_dict() for user in users]

        users_json = {'users': users_lst}

        return self.render_to_json(users_json, request_handler)

    @authenticated
    def user(self, user, **kw):
        request_handler = kw.get('request_handler')

        if kw.get('username'):
            username = kw.get('username')

            session = meta.get_session()
            user_db = session.query(User).filter(User.username==username).first()

            if not user_db:
                return self.render_to_json({"status": "error", "msg": "User not found."}, request_handler)

            return self.render_to_json({'user': user_db.as_dict()}, request_handler)

        else:
            return self.render_to_json({'user': user.as_dict()}, request_handler)


class RescueLoginHandler(BaseHandler):
    """
        Controller de Recuperação de Senha de um Usuário
    """

    def get(self, **kw):
        """
        <h2><b>Recuperar Senha do Usuário</b></h2><br>
        Serviço que regera a senha do usário e envia para o email cadastrado.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        username: username do usuário
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação. O usuário receberá um email com a nova senha.
        """
        
        self.post(**kw)
        
    def post(self, **kw):
        
        username = self.request.GET[u'username']
        session = meta.get_session()        
        user = session.query(User).filter(User.username==username).first()
        
        if user:
            password = self.create_random_passord()
            
            m = hashlib.sha1()
            m.update(password)
            
            user.password = 'sha1$$'+m.hexdigest()
            user.save()

        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps({'status':'ok', 'msg':'Password re-created! Verify you email account'})) 
            
    
        body="""
              Dear %s: <br />
               <br />
              Your new password is %s. We strongly recommend you change as soon as possible. <br />
               <br />
              Please let us know if you have any questions. <br />
               <br />
              The MSS Team
              """ % (user.first_name, password)
        
        try:
            mensagem=EmailHelper.mensagem(destinatario=user.username,corpo=body,strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>',subject="Your account has been created")
            EmailHelper.enviar(mensagem=mensagem,destinatario=user.username)

        except SMTPException, e:
            logging.exception(str(e))
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({'status':'error', 'msg':'Inexistent username'}))
        
        return    
