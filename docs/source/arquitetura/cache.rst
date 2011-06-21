Infraestrutura de Cache
=======================

Para evitar que as requisições do usuário cheguem ao banco de dados ou até mesmo à aplicação python, foram implementados 3 níveis de cache:
	* nginx: cache em disco
	* memcached: armazena objetos e listagem de ids de objetos
	* cache de sessão do SQLAlchemy: armazena os objetos das classes de acesso à banco
	

NGINX
-----

Primeira camada de cache, o nginx pode ser configurado para salvar em disco a resposta a uma determinada requisição.
Podem ser definidas diferentes zonas de cache, cada uma com uma configuração específica de tempo de expiração e tamanho máximo da zona.

Abaixo, um exemplo da configuração realizada para a chamada /status.html ou /webview.html:

.. code-block:: bash

	proxy_cache_path /opt/cache/nginx/status levels=1:2:2 keys_zone=status:200m inactive=10m max_size=2000m;

	# cache zone:status status, webview
	location ~ ^/(status|webview)\.html$ {
	    proxy_pass http://mss-be-upstream;

	    proxy_set_header Host $http_host;
	    proxy_set_header X-Real-IP $remote_addr;
	    proxy_set_header X-Scheme $scheme;

	    proxy_pass_header Server;
	    proxy_redirect off;

	    proxy_cache status;
	    proxy_cache_key "$uri";
	    proxy_cache_valid 200 10d;
	} 

Neste exemplo, o cache será de 10 dias (10d). Será gerado um hash com a url requisitada e a resposta será salva no diretório
definido em proxy_cache_path. O nginx possui uma heurística para criar os diretórios de cache, criando subdiretórios
de acordo com a primeira letra do hash criado.

Memcached
---------

Diferente do nginx, o memcached utiliza cache em memória e compõe a segunda camada de cache do Mobile Social Share, responsável por
armazenar respostas de requisição ao banco. Ele recebe um par <chave>,<valor> e o armazena em memória.

Para diminuir o espaço utilizado em memória, ao invés de armazenar o resultado de uma requisição ao banco, armazena-se a lista de ids
retornadas e, para cada id, armazena-se o objeto retornado (que pode ser utilizado em requisições de outros controllers). Exemplo:
usuário requisita de listagem de todos os amigos. Será salvo no memcached a lista de ids encontrados (e somente ids) e, a partir de cada
id, será salvo o objeto completo. Assim, se fizermos uma requisição ao controller que retorna um amigo específico, por exemplo, este
objeto já estará em memória.

Esse processo também aumenta a performance do sistema. Caso uma lista de objetos (e não de ids) seja armazenada, se alterarmos um objeto
deveríamos expirar a lista inteira. Da maneira proposta no MSS, expiramos apenas o objeto (o id jamais muda) e a atualização refletirá por
todos os serviços que compartilham o objeto.

SQLAlchemy
----------

Realiza o cache em sessão de qualquer objeto criado. Exemplo: ao criarmos um objeto do tipo User, ele é criado, em um primeiro momento, apenas
na sessão do SQLAlchemy. Ao finalizarmos as operações com este objeto, ele é inserido no banco. Assim, a próxima requisição que necessitar
deste objeto, o encontrá na sessão. O SQLAlchemy implementa uma flag de validade do objeto, ou seja, se alguém alterar o objeto essa flag
possuirá um valor indicando isto e o objeto será inserido no banco e atualizado na sessão.