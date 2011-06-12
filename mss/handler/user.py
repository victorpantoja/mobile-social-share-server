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

class UserHandler(BaseHandler):
    
    @authenticated
    def get(self, user, **kw):
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
    
    @authenticated
    def get(self, user, **kw):
        self.post(user, **kw)
        
    def post(self, user, **kw):
        
        username = self.get_argument('username')
        
        session = meta.get_session()  
        users = session.query(User).filter(User.username.like("%"+username+"%")).order_by(User.first_name).all()
                
        users_lst = [user.as_dict() for user in users]
        
        dict = {'users':users_lst}
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return

class LoginHandler(BaseHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        session = meta.get_session()        
        user = session.query(User).filter(User.username==username).first()
        
        m = hashlib.md5()
        m.update(password)
        
        password = m.hexdigest()
                        
        if user and (user.password == password):
            
            auth = hashlib.md5()
            auth.update('%s' % getrandbits(32))
            
            cache = get_cache()
            cache.set(auth.hexdigest(), '%s' % user.username)
            
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'ok', 'msg':auth.hexdigest()}))   
            
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Wrong username or password.'}))
            return

class RescueLoginHandler(BaseHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        
        username = self.request.GET[u'username']
        session = meta.get_session()        
        user = session.query(User).filter(User.username==username).first()
        
        if user:
            password = self.create_random_passord()
            
            m = hashlib.md5()
            m.update(password)
            
            user.password = m.hexdigest()
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
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
                
        user = User()
        user.username = self.get_argument('username')
        
        try:
            EmailHelper.validateEmail(user.username)
        except Exception, e:
            logging.exception(e);
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Invalid email.'}))
            return
        
        user.first_name = self.get_argument('firstName')
        user.last_name = self.get_argument('lastName')
        user.gender = self.get_argument('gender')
        
        password = self.create_random_passord()
        
        m = hashlib.md5()
        m.update(password)
        
        user.password = m.hexdigest()
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
            mensagem=EmailHelper.mensagem(destinatario=user.username,corpo=body,strFrom='Mobile Social Share Team <mobile.social.share@gmail.com>',subject="Your account has been created")
            EmailHelper.enviar(mensagem=mensagem,destinatario=user.username)

        except SMTPException, e:
            logging.exception(str(e))
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':'Account Created! Verify you email account'}))
        return
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        
