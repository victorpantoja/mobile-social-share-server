Arquitetura de Software
=======================

Componentes
-----------

Cada componente da arquitetura do Mobile Social Share foi escolhido tendo em vista alcançar excelentes resultados de performance.

Nginx é um servidor HTTP de alta performance com código aberto e totalmente livre. Foi criado em 2002, pelo russo Igor Sysoev, e teve seu primeiro release liberado em 2004. O Nginx é usado em 6.55% (13.5M) dos domínios ativos no mundo, e esse número vem crescendo exponencialmente.

O Nginx é conhecido por ser muito rápido, estável, com uma grande variedade de módulos, com uma configuração muito simples além de consumir poucos recursos computacionais, como CPU e memória. Ele vem sendo utilizado em diversas aplicações, desde de um simples blog pessoal rodando em um VPS com recursos limitados, até aplicações críticas de alta disponibilidade.

Diferente do servidores tradicionais, nginx não utiliza threads para estabelecer conexões. Ao invés disso, ele utiliza uma arquitetura assíncrona, muito mais escalável, orientada a eventos. Isso permite que ele atenda a milhares de conexões simultâneas com pouco uso de memória e cpu. Essa arquitetura orientada a eventos é conhecida como Asynchronous non-blocking I/O e foi concebida em resposta ao The C10K problem (http://www.kegel.com/c10k.html).

* Nginx
	* Baixo consumo de recursos
	* Simples configuração
	* Alta performance
	* Free e Open Source
	* Proxy Cache
	* Proxy com balanceamento de carga (round-robin ou iphash) com fail-over

Abaixo, uma comparação do nginx com outros servidores HTTP

.. image :: ../img/nginx_benchmark.png

Curva de crescimento na utilização do nginx:

.. image :: ../img/nginx_growing.png


Outro componente importante é o Tornado, um framework bem enxuto com um poderoso web server non-blocking e muito simples de ser implementado. Suas principais características são:

* Tornado
	* Simples
	* Alta performance
	* Leve
	* Open Source
	* Non-blocking I/O
	* Baixo consumo de recursos
	
O gráfico abaixo apresenta um benchmark entre a utlização do nginx + tornado e as implementações mais comuns para aplicações web Python:

.. image :: ../img/tornado_benchmark.png

Outros componentes:
	* SQLAlchemy: camada de acesso ao banco de dados (ORM)
	* Mako: gerenciador de templates
	* Capistrano: ferramenta de deploy automatizado
	* memcached: cache de dados em memória
	* simple-db-migrate: essa ferramenta torna possível que o banco de dados seja facilmente alterado e que cada versão seja bem identificada.

A figura abaixo resume a tecnologia utilizada no Mobile Social Share:

.. image :: ../img/tecnologias.png

Arquitetura Modular
-------------------

No Mobile Social Share, uma instância de nginx distribui a carga para múltiplas instâncias do Tornado. A quantidade de instâncias
depende das configurações do servidor e é diretamente proporcional à quantidade de núcleos do processador. O conjunto nginx + tornados
é definida por "box":

.. image :: ../img/box.png

Na figura acima, estão representadas múltiplas instâncias do memcached, que podem estar em qualquer servidor.

Se dermos um "close" na arquitetura descrita acima e examinarmos apenas a aplicação python, ela será composta pelas seguintes partes:

.. image :: ../img/aplicacao.png

O Tornado recebe a requisição enviada pelo nginx e repassa para o controller específico. Esse controller pode acessar as classses de
repositório ou renderizar diretamente um template.

As classes de repositório buscam os dados no cache e, se não encontrarem, realizam um acesso ao banco de dados.


Arquitetura "Real" do Mobile Social Share
-----------------------------------------

Até este momento, o Mobile Social Share foi descrito de forma isolada, ou seja, apenas um box. No entanto, conjuntos de boxes podem
ser configurados em dezenas de máquinas, conforme a figura abaixo:

.. image :: ../img/arquitetura_completa.png

Essa arquitetura modular possui uma característica bastante importante: pode-se prever a quantidade de máquinas necessárias para
aguentar a quantidade desejada de carga. Em outras palavras, se cada box aguentar, por exemplo, 250 requisições por segundo (req/s)
e a carga desejada é de 2500 req/s serão necessárias 10 máquinas.