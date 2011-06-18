Plataforma de Testes
====================

Introdução
----------

O libby possui uma camada de testes que cobre tanto código python como javascript. Os testes estão divididos usando a seguinte nomenclatura:

* Unitários - Testes que não utilizam recursos de terceiros (Filesystem, Banco de Dados, Índices, etc)
* Funcionais - Testes "wired", isto é, que testam o código integrado aos recursos reais que a aplicação precisa
* Javascript - Testes javascript que comprovam o funcionamento da nossa camada client-side.

Executando os Testes
====================

Unitários
---------

Para executar os testes unitários, utilize o comando::

    make unit

Ao término deste comando, na pasta ./cover do seu projeto estará um arquivo com as estatísticas de cobertura de testes unitários do libby.

Funcionais
----------

Para executar os testes funcionais, utilize o comando::

    make func

Ao término deste comando, na pasta ./cover do seu projeto estará um arquivo com as estatísticas de cobertura de testes funcionais do libby.

Javascript
----------

Para executar os testes de javascript é necessário instalar o `nodejs <http://nodejs.org/#download>`_ e o `npm <http://github.com/isaacs/npm>`_.

Após instalá-los, execute o seguinte comando a partir da pasta raiz do projeto:

.. code-block:: bash

    make setup

Verifique que tudo foi instalado corretamente utilizando::

    npm --version
    node --version

Agora para executar os testes, utilize um dos comandos abaixo::

    make js - roda os testes de javascript no console

    make js-browser - roda os testes de javascript no browser
