Deployment
==========

O deploy da aplicação, ou seja, a subida do código para o servidor, é feita com a ferramenta Capistano.

.. code-block:: bash

	$ cap deploy
	
Com esse simples comando, o código é copiado para o servidor que é, então, reiniciado (tornado e nginx) e a documentação é gerada.