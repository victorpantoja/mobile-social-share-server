# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.handler.base import BaseHandler, authenticated
from mss.models.friendship import Friendship
from mss.models.invite import Invite
from mss.models.user import User
from sqlalchemy.exceptions import IntegrityError
from sqlalchemy.sql.expression import and_

from datetime import datetime
from mss.models import invite_email
from mss.models.invite_email import InviteEmail
from mss.utils.emailhelper import EmailHelper
from smtplib import SMTPException

import logging, hashlib, simplejson

class SendInviteHandler(BaseHandler):
    """
        Controller de Envio de Convite por Sistema
    """
    
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Enviar Convite para Um Usuário Cadastrado</b></h2><br>
        Serviço que enviar um convite para um usuário cadastrado<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        username: username do amigo a ser convidado <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):

        username = self.get_argument('username')
        
        session = meta.get_session()  
        friend = session.query(User).filter(User.username==username).first()
        
        friendship = session.query(Friendship).filter(Friendship.user_id==user.id).filter(Friendship.friend_id==friend.id).first()

        if friendship:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "User is already your friend."})) 
            return

        if not friend:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "User not found."})) 
            return
        
        if friend.id == user.id:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "You cannot be a friend of yourself!"})) 
            return

        invite = Invite()
        invite.user_id = user.id
        invite.friend_id = friend.id
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
    """
        Controller de Obtenção de Todos os Convites que um Usuário Enviou
    """
        
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Obtem os convites envidados por um usuário.</b></h2><br>
        Serviço que obtem os convites envidados por um usuário.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com todos os convites encontrados.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):
        session = meta.get_session()
        
        invites = session.query(Invite).filter(Invite.user_id==user.id).all()
                
        invites_lst = [invite.friend.as_dict() for invite in invites]
        
        dict = {'invite':invites_lst}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return
    
class GetInvitationHandler(BaseHandler):
    """
        Controller de Obtenção de Todos os Convites que um Usuário Recebeu
    """
        
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Obtem os convites pendentes de um usuário.</b></h2><br>
        Serviço que obtem os convites pendentes de um usuário.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com todos os convites encontrados.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):
        session = meta.get_session()
        
        invites = session.query(Invite).filter(Invite.friend_id==user.id).all()
                
        invites_lst = [invite.user.as_dict() for invite in invites]
        
        dict = {'invite':invites_lst}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return
    
class SendEmailInviteHandler(BaseHandler):
    """
        Controller de Envio de Convite por Email
    """    
    
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Enviar Convite por Email para Um Usuário Não Cadastrado</b></h2><br>
        Serviço que envia um convite por email para um usuário não cadastrado<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        email: email do amigo a ser convidado <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):
        
        m = hashlib.md5()
        m.update("%s%s" % (self.get_argument('email'),user.id))
        
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
            mensagem=EmailHelper.mensagem(destinatario=self.get_argument('email'),corpo=body,strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>',subject="Join us at Mobile Social Share")
            EmailHelper.enviar(mensagem=mensagem,destinatario=self.get_argument('email'))

        except SMTPException, e:
            logging.exception(str(e))
            
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
    """
        Controller que Gerencia O Aceite de Convites de Sistema
    """
        
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Aceita um determinado convite enviado por sistema.</b></h2><br>
        Serviço que aceita um determinado convite enviado por sistema..<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        id: ID do convite <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):
                        
        username = self.get_argument('username')
        
        session = meta.get_session()
        friend = session.query(User).filter(User.username==username).first()
        
        if not friend:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "Inexistent user!"}))
            return
        
        invite = session.query(Invite).filter(and_(Invite.user_id==friend.id,Invite.friend_id==user.id)).first()

        if not invite:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({"status": "error", "msg": "Invite not found."}))  
            return
        
        if invite.friend_id == user.id:
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
            
            invite.delete()
            
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({"status": "ok", "msg": "User %s is now your friend!" % friend.first_name}))  
        return
    
class AcceptEmailInviteHandler(BaseHandler):
    """
        Controller que Gerencia o Aceite de Convites por Email
    """
        
    def get(self, **kw):
        """
        <h2><b>Aceita um determinado convite enviado por email.</b></h2><br>
        Serviço que aceita um determinado convite enviado por email.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        code: código do convite <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação.
        """
        
        self.render_template("create_login.html",code=self.get_argument('code'))
