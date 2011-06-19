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


Atualmente, a cobertura de testes está próxima dos 80%. Isso se deve principalmente a funcionalidades de terceiros.

.. code-block:: bash

	$ make functional
	Cleaning up build, *.pyc files...
	Starting memcached...
	Running functional tests...

	test_send_context (mss.tests.functional.handler.test_context.ContextHandlerTestCase) ... ok
	test_get_friendship (mss.tests.functional.handler.test_friendship.FriendshipHandlerTestCase) ... ok
	test_remove_friendship (mss.tests.functional.handler.test_friendship.FriendshipHandlerTestCase) ... ok
	test_remove_inexistent_friendship (mss.tests.functional.handler.test_friendship.FriendshipHandlerTestCase) ... ok
	test_remove_inexistent_friendship_with_inexistent_user (mss.tests.functional.handler.test_friendship.FriendshipHandlerTestCase) ... ok
	test_remove_myself_friendship (mss.tests.functional.handler.test_friendship.FriendshipHandlerTestCase) ... ok
	test_accept_duplicated_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_accept_email_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_accept_inexistent_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_accept_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_get_invites (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_send_duplicate_email_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_send_email_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_send_invite (mss.tests.functional.handler.test_invite.InviteHandlerTestCase) ... ok
	test_get_networks (mss.tests.functional.handler.test_networks.NetworkHandlerTestCase) ... ok
	test_can_login (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_create_existent_user (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_create_user (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_get_other_inexistent_user (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_get_other_user (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_get_user_myself (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	test_search_user (mss.tests.functional.handler.test_user.UserHandlerTestCase) ... ok
	mss.tests.functional.models.test_user.test_user_can_be_saved ... ok
	mss.tests.functional.utils.test_encoding.test_can_smart_encode ... ok
	mss.tests.functional.utils.test_encoding.test_can_smart_encode_numbers ... ok
	mss.tests.functional.utils.test_encoding.test_can_force_unicode ... ok
	mss.tests.functional.utils.test_encoding.test_can_smart_str ... ok
	mss.tests.functional.utils.test_encoding.test_can_smart_str_numbers ... ok
	mss.tests.functional.utils.test_encoding.test_can_smart_str_only ... ok
	mss.tests.functional.utils.test_shorten.test_can_shorter ... ok

	Name                       Stmts   Exec  Cover   Missing
	--------------------------------------------------------
	mss                            3      3   100%   
	mss.core                       1      1   100%   
	mss.core.cache                14      6    42%   22-26, 30-34
	mss.core.cache.backend        47     37    78%   22-23, 35-37, 55-56, 60-62
	mss.core.cache.extension      74     27    36%   11, 13-16, 19-22, 24-26, 29-33, 47-50, 54, 57-58, 61-63, 65, 67-70, 78-82, 86, 90-99, 107, 109-117
	mss.core.cache.util           51     32    62%   19-38, 41-46, 57
	mss.core.exception             2      2   100%   
	mss.core.meta                 43     35    81%   33, 36-39, 44-46
	mss.handler                    1      1   100%   
	mss.handler.base              44     28    63%   21, 24-34, 37, 40, 43, 46-47, 58-60
	mss.handler.context           35     16    45%   54-78
	mss.handler.friendship        41     41   100%   
	mss.handler.invite           118    113    95%   134, 245, 249-251
	mss.handler.network           15     15   100%   
	mss.handler.user             124    115    92%   151, 165, 222-226, 267-268
	mss.models                     1      1   100%   
	mss.models.base               52     41    78%   31, 34, 50-53, 57-62
	mss.models.friendship         13     13   100%   
	mss.models.invite             14     14   100%   
	mss.models.invite_email       13     13   100%   
	mss.models.network            10     10   100%   
	mss.models.user               17     17   100%   
	mss.utils                      1      1   100%   
	mss.utils.emailhelper         36     36   100%   
	mss.utils.encoding            46     26    56%   8-9, 12-13, 23, 45-59, 66-67, 81-88, 92
	mss.utils.shorten_url         13     13   100%   
	--------------------------------------------------------
	TOTAL                        829    657    79%   
	----------------------------------------------------------------------
	Ran 30 tests in 4.995s

	OK