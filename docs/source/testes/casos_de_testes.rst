Casos de Teste
==============

O projeto foi desenvolvido usando a prática ágil conhecida como TDD (Test Driven Development), garantindo um bom design de código e
uma grande cobertura por testes.

Os casos de testes são:

* Usuário envia um contexto
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições
	

* Usuário cria um perfil no sistema
	* Pré-condições: perfil ainda não existe no sistema
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário cria um perfil já existente no sistema
	* Pré-condições: o username já existe no sistema
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de perfil já existente
	* Pós-condições

* Usuário obtém as Redes Sociais disponíveis
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com as redes sociais disponíveis
	* Pós-condições

* Usuário realiza o login no sistema
	* Pré-condições: usuário possui perfil no sistema
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com o token do usuário
	* Pós-condições

* Usuário realiza uma busca por outros usuários
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com a listagem dos usuários que se encaixem na query de busca
	* Pós-condições

* Usuário obtém informações sobre outro usuário
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com as informações do usuário desejado
	* Pós-condições

* Usuário obtém informações sobre si
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com as informações do próprio usuário
	* Pós-condições

* Usuário obtém informações sobre um usuário inexistente
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de usuário inexistente
	* Pós-condições
	
* Usuário adiciona um amigo
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário remove um amigo
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados
	* Pós-condições

* Usuário remove uma amizade inexistente com algum usuário do sistema
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de amizade inexistente
	* Pós-condições

* Usuário remove uma amizade inexistente com algum usuário inexistente do sistema
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de usuário inexistente
	* Pós-condições

* Usuário tenta remover amizade consigo mesmo
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de impossibilidade de remover a amizade
	* Pós-condições

* Usuário obtém sua lista de amigos
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma listagem dos amigos encontrados
	* Pós-condições

* Usuário aceita um convite de sistema
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário aceita um convite por email
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário aceita um convite duplicado
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite duplicado
	* Pós-condições

* Usuário aceita um convite inexistente
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite inexistente
	* Pós-condições

* Usuário obtém uma listagem de convites pendentes
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com a listagem de convites pendentes
	* Pós-condições

* Usuário envia um convite de sistema
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário envia um convite por email
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de sucesso
	* Pós-condições

* Usuário envia um convite por email duplicado
	* Pré-condições: usuário autenticado
	* Entradas
	* Ação
	* Resultados: o sistema responde um JSON com uma mensagem de erro de convite duplicado
	* Pós-condições