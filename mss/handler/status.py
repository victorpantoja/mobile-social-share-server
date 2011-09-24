# coding: utf-8
#!/usr/bin/env python

from mss.handler.base import BaseHandler

class StatusHandler(BaseHandler):
    """
        Controller de Status do Servidor
    """
       
    def get(self, **kw):
        """
        <h2><b>Obter o status do sistema</b></h2><br>
        Serviço que retorna uma página com uma mensagem aos usuários e servir de canal de comunicação entre o administraor do sistema e o usuário.<br>
        <br><h3><b>Parâmetros:</b></h3><br>
        auth: string de autenticação do usuário no MSS <br />
        <br><h3><b>Retorno:</b></h3><br>
        HTML com a informação cadastrada pelo adminstrador.
        """
        
        self.post(**kw)

    def post(self, **kw):
        
        self.render_template("status.html")