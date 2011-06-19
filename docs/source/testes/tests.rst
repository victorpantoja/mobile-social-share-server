Plataforma de Testes
====================

Introdução
----------

O Mobile Social Share possui uma camada de testes que cobre o código python. Os testes estão divididos usando a seguinte nomenclatura:

* Unitários - Testes que não utilizam recursos de terceiros (Filesystem, Banco de Dados, Índices, etc)
* Funcionais - Testes "wired", isto é, que testam o código integrado aos recursos reais que a aplicação precisa

Executando os Testes
====================

Unitários
---------

Para executar os testes unitários, utilize o comando::

    make unit

Ao término deste comando, na pasta ./cover do seu projeto estará um arquivo com as estatísticas de cobertura de testes unitários do MSS.

Funcionais
----------

Para executar os testes funcionais, utilize o comando::

    make funciontal

Ao término deste comando, na pasta ./cover do seu projeto estará um arquivo com as estatísticas de cobertura de testes funcionais do MSS.
