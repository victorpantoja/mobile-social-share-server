API de Amigos
=============

Obtém os relacionamentos do usuário autenticado
-----------------------------------------------
.. code-block:: python

	(r"/friendship/get.json", GetFriendshipsHandler),

Serviço que retorna os relacionamentos do usuário autenticado.

Parâmetros:
	* auth: string de autenticação do usuário no MSS

Retorno:
	JSON com todos os amigos encontrados.


Remove um Relacionamento
-----------------------------------------------
.. code-block:: python

	(r"/friendship/remove", RemoveFriendshipsHandler),

Serviço que retorna uma página com uma mensagem aos usuários e servir de canal de comunicação entre o administraor do sistema e o usuário.

Parâmetros:
	* auth: string de autenticação do usuário no MSS
	* username: username do amigo a ser removido

Retorno:
	JSON com o status da ação.