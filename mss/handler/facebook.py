# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler
from mss.core.cache import get_cache
from mss.utils.curl import MSSCurl

import urlparse, simplejson


class CanvasHandler(BaseHandler):
    """
        Controller de Exibição das Informações de Contexto no Facebook
    """
    
    def get(self, **kw):
        """
        <h2><b>Exibe as informações de Contexto Enviadas pelos Usuários de Forma Integrada ao Facebook</b></h2><br>
        Serviço que retorna uma página com as informações de contexto enviadas pelos usuários<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        Nenhum
        <br><h3><b>Retorno:</b></h3><br>
        Página HTML Integrada ao Google Maps exibindo as informações de contexto enviadas pelos usuários e sua posição.
        """
        
        self.post(**kw)

    def post(self, **kw):

        cache = get_cache()
        locale = cache.get("locale")
        content = cache.get("content")

        self.render_template("facebook/canvas.html",locale=locale, content=content)


class AuthorizationHandler(BaseHandler):

    def get(self, **kw):
        
        code = self.get_argument('code')
        
        client_id = '113400205406273'
        secret = '26cfa7320bf675ea1288522178a45bb5'
        redirect_uri = 'http://myalbumshare.com:9080/auth'
        
        url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' % (client_id, redirect_uri, secret, code)
        
        data = MSSCurl().get(str(url),'plain')
        
        response = urlparse.parse_qs(data)
                
        self.set_header("Content-Type", "application/json; charset=UTF-8")                
        self.write(simplejson.dumps(response))
        
        return
