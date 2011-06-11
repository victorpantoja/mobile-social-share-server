Instalação
============

A instalação do libby é feita usando o pip e o mirror de pypi da globo.com.

.. warning::

    É necessária a utilização do pip versão 0.8.1 ou superior

.. note::

    Para saber a versão do seu pip execute: **pip --version**

.. note::
    
    Para atualizar seu pip execute: **pip install -U pip**

Agora instale o libby usando o pip:

.. code-block:: bash

    pip install globo-libby --use-mirrors --mirrors="http://pypi.glb.com"

Verifique que a instalação funcionou utilizando o interpretador python (a versão que será exibida depende de qual você instalou):

.. code-block:: python

    >>> import libby
    >>> print libby.__version__
    0.6.10

Continuous Integration
----------------------

O CI do libby pode ser visto através da URL `<http://pp.glb.com/>`_.

Instalação de URLS
------------------

Além disso, é necessário incluir nas urls do projeto as urls do libby.

Caso você utilize a `aplicação de publicação em múltiplos dispositivos
<aplicacoes/publicacao_multi_dispositivos.html>`_,
é necessária a inclusão, ainda, das urls de dispositivos, como se segue:

.. code-block:: python

    urlpatterns = patterns('',
        #...

        url('^libby/', include('libby.urls')),
        
        #esta url abaixo é opcional. é necessária se a aplicação
        #de publicação multi-dispositivos estiver em uso
        url('^/', include('libby.device_urls')),

        #...
    )

.. warning::

    O libby PRECISA ser incluído antes do globocore nas urls, pois o globocore
    possui uma regra inclusiva que mapeia TUDO que não for /admin.

Instalação de Tamanhos de Foto
------------------------------

Para garantir que os tamanhos de foto requeridos pelos destaques, agrupadores
e componentes do Libby funcionem automaticamente, basta executar o extensor de
tamanhos de foto do libby, conforme abaixo:

.. code-block:: python

    #início do settings
    from libby.photo import extend_photo_sizes

    #Última coisa do Settings - precisa estar após INSTALLED_APPS e
    #DESKTOP_PHOTO_SIZES.
    extend_photo_sizes(INSTALLED_APPS, DESKTOP_PHOTO_SIZES)

    #onde INSTALLED_APPS é a lista de apps instaladas do Django
    #e DESKTOP_PHOTO_SIZES é a coleção de tamanhos de foto da plataforma.

