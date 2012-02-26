# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import get_cache
from mss.handler.base import BaseHandler, authenticated
from mss.models.user import User
from mss.utils.emailhelper import EmailHelper
from mss.utils.encoding import smart_unicode

from datetime import datetime
from random import choice, getrandbits
from smtplib import SMTPException
import logging, hashlib, string, simplejson
from mss.models.invite_email import InviteEmail
from mss.models.friendship import Friendship
from mss.models.invite import Invite

class UserHandler(BaseHandler):
    """
        Controller de Obtenção das Informações de um Usuário
    """
    
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Obter as informações de um usuário</b></h2><br>
        Serviço que retorna as informações disponíveis de um usuário.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        username (opcional): username do usuário. Se não for passado, será utilizado o username do usuário autenticado.
        <br><h3><b>Retorno:</b></h3><br>
        JSON representando o usuário.
        """
        
        self.post(user,**kw)
        
    def post(self, user, **kw):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
                
        if self.get_arguments('username'):
            username = self.get_argument('username')
            
            session = meta.get_session()  
            user_db = session.query(User).filter(User.username==username).first()
            
            if not user_db:
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(simplejson.dumps({"status": "error", "msg": "User not found."})) 
                return
            
            self.write(simplejson.dumps({'user':user_db.as_dict()}))
            
        else:
            self.write(simplejson.dumps({'user':user.as_dict()}))
        
        return
    
class UserSearchHandler(BaseHandler):
    """
        Controller de Busca de Usuários
    """
        
    @authenticated
    def get(self, user, **kw):
        """
        <h2><b>Buscar Usuários</b></h2><br>
        Serviço que retorna os usuários que correspondem a busca realizada.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        username: palavra de busca.
        <br><h3><b>Retorno:</b></h3><br>
        JSON representando o usuário.
        """
        
        self.post(user, **kw)
        
    def post(self, user, **kw):
        
        username = self.get_argument('username')
        
        #TODO - Escape
        session = meta.get_session()  
        users = session.query(User).filter(User.username.like("%"+username+"%")).order_by(User.first_name).all()
                
        users_lst = [user.as_dict() for user in users]
        
        dict = {'users':users_lst}
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return

class LoginHandler(BaseHandler):
    """
        Controller de Autenticação de um Usuário
    """
    
    def get(self, **kw):
        """
        <h2><b>Autenticar Usuário</b></h2><br>
        Serviço que autentica um usuário e retorna um token (auth).<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        Nenhum
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação e o token (auth) de autenticação do usuário.
        """
        
        self.post(**kw)
        
    def post(self, **kw):
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        session = meta.get_session()        
        user = session.query(User).filter(User.username==username).first()
        
        m = hashlib.sha1()
        m.update(password)
        
        password = 'sha1$$'+m.hexdigest()
                        
        if user and (user.password == password):
            
            auth = hashlib.md5()
            auth.update('%s' % getrandbits(32))
            
            cache = get_cache()
            cache.set(auth.hexdigest(), '%s' % user.username)
            
            invites = session.query(Invite).filter(Invite.friend_id==user.id).all()
            invites_lst = [invite.user.as_dict() for invite in invites]
            
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'ok', 'msg':auth.hexdigest(),'invites':invites_lst}))   
            
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Wrong username or password.'}))
            return

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
        
class CreateLoginHandler(BaseHandler):
    """
        Controller de Criação de um Novo Usuário
    """
        
    def get(self, **kw):
        """
        <h2><b>Criação de Usuário</b></h2><br>
        Serviço que cria um usuário no sistema.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        username: username do usuário
        firstName: nome do usuário
        lastName: sobrenome do usuário
        gender: gênero do usuário F (Feminino), M (Masculino), O (Outro)
        <br><h3><b>Retorno:</b></h3><br>
        JSON com o status da ação. O usuário receberá um email com a senha gerada.
        """
        
        self.post(**kw)

    def post(self, **kw):
                
        user = User()
        user.username = self.get_argument('username')
        user.email = self.get_argument('email')
        user.is_staff = True
        user.is_superuser = False
        user.is_active = True
        
        try:
            EmailHelper.validateEmail(user.email)
        except Exception, e:
            logging.exception(e);
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Invalid email.'}))
            return
        
        user.first_name = self.get_argument('firstName')
        user.last_name = self.get_argument('lastName')
        user.gender = self.get_argument('gender')
        
        password = self.create_random_passord()
        
        m = hashlib.sha1()
        m.update(password)
        
        user.password = 'sha1$$'+m.hexdigest()
        user.created = datetime.now()
        user.last_login = datetime.now()
        

        body="""
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
            logging.exception(e);
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Username already exists.'}))
            return
        
        try:
            mensagem=EmailHelper.mensagem(destinatario=user.email,corpo=body,strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>',subject="Your account has been created")
            EmailHelper.enviar(mensagem=mensagem,destinatario=user.email)

        except SMTPException, e:
            logging.exception(str(e))
            
        code = self.get_argument("code", "")
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
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':'Account Created! Verify you email account'}))
        return
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        
