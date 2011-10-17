# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.core.cache import get_cache
from mss.models.application import Application
from mss.models.context_type import ContextType
from mss.models.context import Context
from mss.models.context_application import ContextApplication
from mss.utils.context import ContextQueue

from datetime import datetime

import simplejson

class WebViewHandler(BaseHandler):
    """
        Controller de Exibição dos Contextos
    """
    
    def get(self, **kw):
        """
        <h2><b>Exibe as informações de Contexto Enviadas pelos Usuários</b></h2><br>
        Serviço que retorna uma página com as informações de contexto enviadas pelos usuários<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        Página HTML Integrada ao Google Maps exibindo as informações de contexto enviadas pelos usuários e sua posição.
        """
        
        self.post(**kw)

    def post(self, **kw):

        cache = get_cache()
        locale = cache.get("locale")
        content = cache.get("content")

        self.render_template("facebook/webview.html",locale=locale, content=content)

class ContextHandler(BaseHandler):
    """
        Controller de Envio de Contexto para as Redes Sociais
    """
    
    @authenticated
    def get(self, user, **kw):
        contexts = Context().all()
        
        contexts_lst = [context.as_dict() for context in contexts]
        
        contexts_dict = {'contexts':contexts_lst}
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps(contexts_dict))
        return

    @authenticated
    def post(self, user, **kw):
        """
        <h2><b>Recebe o contexto enviado por um usuário e distribui pelas redes sociais.</b></h2><br>
        Serviço que Recebe o contexto enviado por um usuário e distribui pelas redes sociais selecionadas.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com Status da Ação e Cópia da Mensagem Enviada para as Redes Sociais
        """
                                
        data = simplejson.loads(self.request.body)
        
        for app_name in data['application']:
            application = Application().get_by(name=app_name)
            
            if application:
                for description in data['context'].keys():
                    context_type = ContextType().get_by(description=description)
                    
                    if context_type:
                        context = Context()
                        context.user_id = user.id
                        context.context_type_id = context_type.id
                        context.context = data['context'][description]
                        context.updated = datetime.now()
                        context.save()
                        
                        context_application = ContextApplication()
                        context_application.application = application
                        context_application.context = context
                        context_application.save()
                    else:
                        self.set_header("Content-Type", "application/json; charset=UTF-8")
                        self.write(simplejson.loads({'status':'error', 'msg':"Context Not Sent. Invalid context-type."}))
                        self.finish()
                        return                     
                                
                ContextQueue().add(application.name,data['context'], application.callback_url)
            else:
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(simplejson.dumps({'status':'error', 'msg':"Context Not Sent. Application not registered."}))
                self.finish()
                return
                        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':"Context Sent"}))
        self.finish()
        return

class ContextTestHandler(BaseHandler):
    def get(self, **kw):
        self.post(**kw)
        
    def post(self, **kw):
        
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(simplejson.dumps({'status':'ok', 'msg':"Context Received"}))
        self.finish()
        return
        