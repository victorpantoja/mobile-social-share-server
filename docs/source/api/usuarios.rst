API de Usuário
==============

Criação de Usuário
------------------

.. code-block:: python

	(r"/login/create", CreateLoginHandler),

Serviço que cria um usuário no sistema.

Parâmetros:
	* username: username do usuário
	* firstName: nome do usuário
	* lastName: sobrenome do usuário
	* gender: gênero do usuário F (Feminino), M (Masculino), O (Outro)

Retorno:
	JSON com o status da ação. O usuário receberá um email com a senha gerada.


Obter as informações de um usuário
----------------------------------
.. code-block:: python

	(r"/user.json", UserHandler),

Serviço que retorna as informações disponíveis de um usuário.

Parâmetros:
	* auth: string de autenticação do usuário no MSS 
	* username (opcional): username do usuário. Se não for passado, será utilizado o username do usuário autenticado.

Retorno:
	JSON representando o usuário.


Buscar Usuários
----------------
.. code-block:: python

	(r"/search/users.json", UserSearchHandler),

Serviço que retorna os usuários que correspondem a busca realizada.

Parâmetros:
	* auth: string de autenticação do usuário no MSS 
	* username: palavra de busca.

Retorno:
	JSON representando o usuário.


Recuperar Senha do Usuário
--------------------------
.. code-block:: python

	(r"/login/rescue", RescueLoginHandler),

Serviço que regera a senha do usário e envia para o email cadastrado.

Parâmetros:
	* username: username do usuário

Retorno:
	JSON com o status da ação. O usuário receberá um email com a nova senha.