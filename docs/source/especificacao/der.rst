Diagrama de Entidades e Relacionamentos
=======================================

O Mobile Social Share usa o modelo lógico de dados representado no seguinte DER:

.. image :: ../img/diagrama_classes.png


Para este DER, temos o seguinte dicionário de dados:

* **users** - Entidade que define os usuários do sistema
	* user_id: identificador único de um usuário
	* username_txt: login do usuário
	* lastname_txt:sobrenome do usuário
	* firstname_txt: primeiro nome do usuário
	* gender_flg: gênero do usuário (masculino, feminino)
	* password_txt: senha do usuário
	* criate_dt: data de criação do usuário
	* lastlogin_dt: data em que o usuário acessou o sistema pela última vez


* **social_network** - Entidade que define as redes sociais
	* network_id: identificador único de uma rede social
	* name_txt: nome da rede social (i.e. Facebook)
	* icon_txt: ícone representativo da rede social
	* available_bln: define se a rede social está ativa ou não


* **context** - Entidade que define os contextos enviados pelos usuários
	* context_id: identificador único de um contexto
	* user_id: id do usuário
	* status_txt: texto enviado pelo usuário, representando um contexto ativo
	* location_txt: coordenadas geográficas do usuário ao enviar o contexto
	* updated_dt: data de atualização do contexto


* **friendship** - Entidade que define os relacionamentos entre os usuários
	* friendship_id: identificador único de um relacionamento entre usuários
	* user_id: id do usuário
	* friend_id: id do usuário com quem user_id se relaciona
	* created_dt: data de criação do relacionamento


* **invite** - Entidade que define os convites enviados através do sistema
	* invite_id: identificador único de um convite de sistema
	* user_id: id do usuário
	* friend_id: id do usuário convidado
	* invite_dt: data de envio do convite


* **invite_email** - Entidade que define os convites enviados por email
	* invite_email_id: identificador único de um convite por email
	* user_id: id do usuário
	* code_txt: código que identifica e valida o email
	* invite_dt: data de envio do convite
