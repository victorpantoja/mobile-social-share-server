# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.core.cache import get_cache
from mss.models.application import Application
from mss.models.context_type import ContextType
from mss.models.context import Context
from mss.models.context_application import ContextApplication
from mss.utils.shorten_url import ShortenURL

from tornado.web import asynchronous
from datetime import datetime

import simplejson, twitter

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
            application = Application().fetch_by(name=app_name).first()
            
            if application:
                for description in data['context'].keys():
                    context_type = ContextType().fetch_by(description=description).first()
                    
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

                
        consumer_key = "f1j3JookvHIoe2MBL7HEg"
        consumer_secret = 'kdgLHtmyFh24UVIDIBtFRC9T5LUlRhgtCskIlG1P08'
        access_token_key = '353770828-OeTG1nMJEuMHIKEdVQvrFloXnI9hcUXBROZ8oyiX'
        access_token_secret = 'u30TQhtFmWB9bKgyXrhJ7SNLGuuxO2n3dJfswv66k'
        
        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
        
        map_url = 'http://maps.google.com/maps?z=18&q=%(location)s(%(text)s)' % {'location':data['context']['location'],'text':data['context']['status']}
        
        shortened = ShortenURL().Shorten(map_url)
        
        status = ''
        
        try:
            status = api.PostUpdate("%s %s #mss" % (data['context']['status'], shortened))
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'ok', 'msg':status.text}))

        except twitter.TwitterError, e:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':e.message}))
            
        self.finish()
        return


