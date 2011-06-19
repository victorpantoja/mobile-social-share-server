Instalação
===========

A instalação do MSS é bastante simples. É necessário apenas que se faça um clone do projeto.

.. warning::

    É necessária a utilização do git

.. note::

    Para saber a versão do seu git execute: **git --version**

.. code-block:: bash

    git clone git@github.com:victorpantoja/mobile-social-share-server.git

Verifique que a instalação funcionou utilizando o interpretador python (a versão que será exibida depende de qual você instalou) a partir da raiz do projeto:

.. code-block:: python

    >>> import mss
    >>> print mss.__version__
    1.0.0

Dependências:
=============

O MSS depende dos seguintes módulos pyton:

------------------
Tornado Web Server
------------------
Tornado is an open source version of the scalable, non-blocking web server and tools that power FriendFeed. The FriendFeed application is written using a web framework that looks a bit like web.py or Google's webapp, but with additional tools and optimizations to take advantage of the underlying non-blocking infrastructure.

.. code-block:: bash

	sudo easy_install tornado

More information:
http://www.tornadoweb.org/

----------
SQLAlchemy
----------
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

More information:
http://www.sqlalchemy.org/

--------------
Mako Templates
--------------
Mako is a template library written in Python. It provides a familiar, non-XML syntax which compiles into Python modules for maximum performance. Mako's syntax and API borrows from the best ideas of many others, including Django templates, Cheetah, Myghty, and Genshi. Conceptually, Mako is an embedded Python (i.e. Python Server Page) language, which refines the familiar ideas of componentized layout and inheritance to produce one of the most straightforward and flexible models available, while also maintaining close ties to Python calling and scoping semantics.

.. code-block:: bash

	sudo easy_install mako

More information:
http://www.makotemplates.org/

------
routes
------
Routes is a Python re-implementation of the Rails routes system for mapping URLs to application actions, and conversely to generate URLs. Routes makes it easy to create pretty and concise URLs that are RESTful with little effort.

Routes allows conditional matching based on domain, cookies, HTTP method, or a custom function. Sub-domain support is built in. Routes comes with an extensive unit test suite.

.. code-block:: bash

	sudo easy_install routes

More information:
http://routes.groovie.org/

--------
memcache
--------
This is a Python based API (implemented in 100% python) for communicating with the memcached distributed memory object cache daemon. 

.. code-block:: bash

	sudo easy_install python-memcached

More information:
http://www.tummy.com/Community/software/python-memcached/

----------
simplejson
----------
Simple, fast, extensible JSON encoder/decoder for Python

.. code-block:: bash

	sudo easy_install simplejson

More information:
http://pypi.python.org/pypi/simplejson/

--------------
python-twitter
--------------
A Python wrapper around the Twitter API

.. code-block:: bash

	sudo easy_install python-twitter

More information:
http://code.google.com/p/python-twitter/

-----------------
simple-db-migrate
-----------------
simple-db-migrate is a database versioning and migration tool inspired on Rails Migrations. 

.. code-block:: bash

	sudo easy_install simple-db-migrate

More information:
http://guilhermechapiewski.github.com/simple-db-migrate/

.. admonition:: migration

    Não se esqueça de rodar as migrations após instalar a app para que o banco de dados seja devidamente criado.