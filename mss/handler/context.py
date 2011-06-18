# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler, authenticated
from mss.core.cache import get_cache
import simplejson, twitter
from mss.utils.shorten_url import ShortenURL

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
        """
        <h2><b>Recebe o contexto enviado por um usuário e distribui pelas redes sociais.</b></h2><br>
        Serviço que Recebe o contexto enviado por um usuário e distribui pelas redes sociais selecionadas.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        JSON com Status da Ação e Cópia da Mensagem Enviada para as Redes Sociais
        """
        
        self.post(user, **kw)

    def post(self, user, **kw):

        cache = get_cache()
        cache.set("locale",self.get_argument('location'))
        cache.set("content",self.get_argument('text'))
        
        consumer_key = "uXTHwPObQdiDANsQNyN9fA"
        consumer_secret = 'pPHWgoiVF1pKynGTM77CCv1G9CUgtD0BfWkqBYhtA'
        access_token_key = '15043020-6FMt90SSPL5coMpTvuTNIjH8Q2hNumSvSEYh2tqXN'
        access_token_secret = 'cdlZNKne6fSMBVgf80YOiC0J6yin4MtCygHfgkSk'
        
        api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
        
        map_url = 'http://maps.google.com/maps?z=18&q=%(location)s(%(text)s)' % {'location':self.get_argument('location'),'text':self.get_argument('text')}
        
        shortened = ShortenURL().Shorten(map_url)
        
        status = ''
        
        try:
            status = api.PostUpdate("%s %s #mss" % (self.get_argument('text'), shortened))
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'ok', 'msg':status.text}))
            return
        except twitter.TwitterError, e:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.write(simplejson.dumps({'status':'error', 'msg':e.message}))            


