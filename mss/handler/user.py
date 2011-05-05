# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import get_cache
from mss.handler.base import BaseHandler
from mss.models.user import User
from mss.utils.emailhelper import EmailHelper

from datetime import datetime
from random import choice, getrandbits
from smtplib import SMTPException
import logging, hashlib, string, simplejson

class LoginHandler(BaseHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        session = meta.get_session()        
        user = session.query(User).filter(User.username==username).first()
                
        if user and (user.password == password):
            
            auth = hashlib.md5()
            auth.update('%s' % getrandbits(32))
            
            cache = get_cache()
            cache.set(auth.hexdigest(), '%s_auth' % user.username)
            
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
        
        user = User()
        user.first_name = "teste"
        user.last_name = "teste"
        
        username = self.request.GET[u'username']
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({'status':'ok', 'msg':'Password re-created! Verify you email account'}))    
        
class CreateLoginHandler(BaseHandler):
    
    def get(self, **kw):
        self.post(**kw)

    def post(self, **kw):
                
        user = User()
        user.username = self.get_argument('username')
        
        user.first_name = self.get_argument('firstName')
        user.last_name = self.get_argument('lastName')
        
        m = hashlib.md5()
        m.update(self.create_random_passord())
        
        user.password = m.hexdigest()
        user.created = datetime.now()
        user.last_login = datetime.now()

        try:
            user.save()
        except:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':'Username already exists.'}))
            return
        
        try:
            mensagem=EmailHelper.mensagem(destinatario='victor.pantoja@gmail.com',corpo='teste',strFrom='MSS Team <victor.pantoja@gmail.com>')
            EmailHelper.enviar(mensagem=mensagem,destinatario='victor.pantoja@gmail.com')

        except SMTPException, e:
            logging.exception(str(e))
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':'Account Created! Verify you email account'}))
        return
        
        
    def create_random_passord(self):
        size = 9
        return ''.join([choice(string.letters + string.digits) for i in range(size)])
        
