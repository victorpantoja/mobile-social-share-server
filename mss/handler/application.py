# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
import simplejson
from mss.core import meta
from mss.models.application import Application

class ApplicationHandler(BaseHandler):
    """
        Controller de Obtenção das Redes Sociais Disponíveis
    """

    @authenticated    
    def get(self, **kw):
        """
        <h2><b>Obter as Redes Sociais Disponíveis</b></h2><br>
        Serviço que retorna as redes sociais disponíveis no sistema.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com todas as redes sociais encontrados.
        """
        
        self.post(**kw)

    def post(self, **kw):
        
        session = meta.get_session()
        
        apps = session.query(Application).all()
        
        app_list = [app.as_dict() for app in apps]
        
        dict = {'applications':app_list}

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(dict))
        return