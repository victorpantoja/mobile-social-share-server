Casos de Teste
==============

O projeto foi desenvolvido usando a prática ágil conhecida como TDD (Test Driven Development), garantindo um bom design de código e
uma grande cobertura por testes.

Os casos de testes são:

* Usuário envia um contexto
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente, redes sociais desejadas e contexto a ser enviado
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: a informAção: usuário acessa o serviço correspondente enviada está disponível na rede social
	

* Usuário cria um perfil no sistema
	* Pré-condições: perfil ainda não existe no sistema
	* Entradas: username, primeiro nome, sobrenome e gênero do usuário
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: perfil passa a existir no sistema. Um email é enviado com a senha do usuário.

* Usuário cria um perfil já existente no sistema
	* Pré-condições: o username já existe no sistema
	* Entradas: username, primeiro nome, sobrenome e gênero do usuário
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de perfil já existente
	* Pós-condições: N/D

* Usuário obtém as Redes Sociais disponíveis
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com as redes sociais disponíveis
	* Pós-condições: N/D

* Usuário realiza o login no sistema
	* Pré-condições: usuário possui perfil no sistema
	* Entradas: username e senha de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com o token do usuário
	* Pós-condições: token do usuário salvo no cache para futuras autenticações

* Usuário realiza uma busca por outros usuários
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente, string de busca
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com a listagem dos usuários que se encaixem na query de busca
	* Pós-condições: N/D

* Usuário obtém informações sobre outro usuário
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e username do usuário
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com as informações do usuário desejado
	* Pós-condições: N/D

* Usuário obtém informações sobre si
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com as informações do próprio usuário
	* Pós-condições: N/D

* Usuário obtém informações sobre um usuário inexistente
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e username do usuário
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de usuário inexistente
	* Pós-condições: N/D
	
* Usuário adiciona um amigo
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e username do usuário a ser adicionado
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: usuários se tornam amigos

* Usuário remove um amigo
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente  e username do usuário a ser removido
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: usuários não são mais amigos

* Usuário remove uma amizade inexistente com algum usuário do sistema
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e username do usuário a ser removido
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de amizade inexistente
	* Pós-condições: N/D

* Usuário remove uma amizade inexistente com algum usuário inexistente do sistema
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e username do usuário a ser removido
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de usuário inexistente
	* Pós-condições: N/D

* Usuário tenta remover amizade consigo mesmo
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e o próprio username
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de impossibilidade de remover a amizade
	* Pós-condições: N/D

* Usuário obtém sua lista de amigos
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma listagem dos amigos encontrados
	* Pós-condições: N/D

* Usuário aceita um convite de sistema
	* Pré-condições: usuário autenticado, convite existente
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e id do convite
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: usuário se torna amigo daquele que lhe enviou o convite

* Usuário aceita um convite por email
	* Pré-condições: usuário autenticado, convite existente
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e código do convite
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o usuário se cadastra no sistema e automaticamente estabelece amizade com quem o convidou
	* Pós-condições: usuários se tornam amigos

* Usuário aceita um convite duplicado
	* Pré-condições: usuário autenticado, convite já existente
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e id do convite
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite duplicado
	* Pós-condições: N/D

* Usuário aceita um convite inexistente
	* Pré-condições: usuário autenticado, convite inexistente
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente e id do convite
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite inexistente
	* Pós-condições: N/D

* Usuário obtém uma listagem de convites pendentes
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com a listagem de convites pendentes
	* Pós-condições: N/D

* Usuário envia um convite de sistema
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente, username do usuário a ser convidado
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: usuário convidado receberá o convite quando acessar o serviço correspondente

* Usuário envia um convite por email
	* Pré-condições: usuário autenticado
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente, email do usuário a ser convidado
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições: usuário convidado receberá o convite no email

* Usuário envia um convite por email duplicado
	* Pré-condições: usuário autenticado, convite já existente
	* Entradas: token de autenticAção: usuário acessa o serviço correspondente
	* Ação: usuário acessa o serviço correspondente
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite duplicado
	* Pós-condições: N/A