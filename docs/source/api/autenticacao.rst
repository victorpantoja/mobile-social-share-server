API de Autenticação
===================

Autenticar Usuário
-------------------

.. code-block:: python

	(r"/login", LoginHandler),

Serviço que autentica um usuário e retorna um token (auth).

Parâmetros: Nenhum

Retorno:
	JSON com o status da ação e o token (auth) de autenticação do usuário.
