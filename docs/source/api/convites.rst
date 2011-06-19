API de Convites
===============

Enviar Convite para Um Usuário Cadastrado
-----------------------------------------

.. code-block:: python

	(r"/invite/send", SendInviteHandler),

Serviço que enviar um convite para um usuário cadastrado

Parâmetros:
	* auth: string de autenticação do usuário no MSS
	* username: username do amigo a ser convidado

Retorno:
	JSON com o status da ação.
	

Aceita um determinado convite enviado por sistema
-------------------------------------------------

.. code-block:: python

	(r"/invite/accept", AcceptInviteHandler),

Serviço que aceita um determinado convite enviado por sistema.

Parâmetros:
	* auth: string de autenticação do usuário no MSS
	* id: ID do convite
	
Retorno:
	JSON com o status da ação.


Obtem os convites envidados por um usuário
------------------------------------------

.. code-block:: python

	(r"/invite/get.json", GetInviteHandler),

Serviço que obtem os convites envidados por um usuário.

Parâmetros:
	* auth: string de autenticação do usuário no MSS

Retorno:
	JSON com todos os convites encontrados.


Enviar Convite por Email para Um Usuário Não Cadastrado
-------------------------------------------------------

.. code-block:: python

	(r"/invite/email/send", SendEmailInviteHandler),

Serviço que envia um convite por email para um usuário não cadastrado

Parâmetros:
	* auth: string de autenticação do usuário no MSS
	* email: email do amigo a ser convidado

Retorno:
	JSON com o status da ação.


Aceita um determinado convite enviado por email
------------------------------------------------

.. code-block:: python

	(r"/invite/email/accept", AcceptEmailInviteHandler),

Serviço que aceita um determinado convite enviado por email.

Parâmetros:
	* id: ID do convite

Retorno:
	JSON com o status da ação.


Obtem os convites pendentes de um usuário
-----------------------------------------

.. code-block:: python

	(r"/invitation/get.json", GetInvitationHandler),


Serviço que obtem os convites pendentes de um usuário.

Parâmetros:
	* auth: string de autenticação do usuário no MSS

Retorno:
	JSON com todos os convites encontrados.
