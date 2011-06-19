Motivação
==========

Recentemente, começou-se a experimentar uma migração das comunidades físicas para comunidades virtuais. As pessoas estão utilizando cada vez mais a Internet para se comunicar e encontrar novos amigos ou relacionamentos afetivos através de sites que promovem a formação de comunidades baseadas em semelhanças nos perfis virtuais dos usuários. Redes Sociais Pervasivas (RSP) representam um novo paradigma de computação, derivado da convergência da Computação Pervasiva com os Serviços de Redes Sociais como o Facebook, Orkut e Twitter [1], que vêm se tornando bastante populares nos últimos anos. O Facebook, por exemplo, possui mais de 500 milhões de usuários ativos que gastam mais de 700 bilhões de minutos por mês navegando na rede [2].

Enquanto isso, a crescente popularização dos dispositivos móveis e de sua capacidade de processamento, armazenamento e sensoriamento criaram um fenômeno de migração parecido no mundo mobile e também provocaram o surgimento de aplicações móveis capazes de interagir com diversas redes sociais. Tais aplicações móveis podem ajudar as pessoas a manterem contato em qualquer lugar, a qualquer hora, além de prover recomendações em tempo real sobre pessoas, lugares e eventos ou entregar conteúdo personalizado em função do contexto geo-social.

Existem duas questões chaves inerentes à troca de informações de contexto que este trabalho pretende resolver. A primeira delas, identificada por Endler et al [3] diz respeito à falta de um padrão de comunicação com as redes sociais, apesar de alguns esforços para neste sentido, como o OpenSocial [4]. Cada rede social fornece sua própria API com padrões diferentes para acessos aos dados. A segunda leva em consideração a ineficiência da transferência de informações entre o dispositivo móvel e os serviços na Internet, i.e. grande quantidade de dados redundantes transferidos, consequentemente, um maior consumo de banda wireless e da energia do dispositivo, no recebimento e processamento desses dados.

Um exemplo prático deste segundo problema é a API de mapas do Google [5]. Uma aplicação que necessite apenas da distância entre dois pontos, ao consultar este serviço, terá como resposta um XML contendo, além da distância desejada, a rota entre esses pontos. Um servidor poderia fazer a ponte entre a API e a aplicação e só repassar o que fosse realmente relevante, diminuindo consideravelmente o tamanho da resposta recebida pela aplicação.

Além das questões acima, este trabalho pretende resolver algumas limitações que as aplicações comparadas possuem tais como conhecimento do status em tempo real do usuário nas redes sociais e integração com as redes sociais para propor novas amizades.  A primeira questão diz respeito à importância de se conhecer a útlima atualização de perfil do usuário para, a partir disso, inferir um contexto social. O usuário poderia, por exemplo, escrever no Twitter que está indo para uma festa e a aplicação utilizar esse contexto para propor uma playlist chamada "Festa" no seu smartphone. A segunda questão refere-se à construção de uma rede social baseada em informações de status e perfis semelhantes. Dois usuários indo para uma mesma festa poderiam receber uma sugestão de amizade em comum e formar uma rede com outros usuários que compartilharam esse mesmo contexto "festa".

Objetivos
==========

O objetivo deste trabalho é desenvolver uma interface genérica para transferência otimizada de informações de contexto entre dispositivos móveis e diferentes redes sociais. Esta interface levará em consideração as atualizações de status do usuário nas redes sociais para identificar mudanças de contexto (por exemplo, identificar que um usuário está indo para uma festa) e será disponibilizada através de uma API genérica, permitindo que aplicações de terceiros sejam construídas com menos esforço utlizando-se qualquer tecnologia e plataforma que suporte o formato JSON, utilizando nas mensagens de resposta do servidor. A generalidade desta interface está em comunicar-se com redes sociais de forma transparente para a aplicação móvel, ou seja, as informações de contexto serão enviadas para as redes sem que a aplicação precise executar os protocolos de comunicação específicos de cada uma delas.

---------------------------
Referências Bibliográficas
---------------------------
[1] Dias Junior, E.P.F..; Rodrigues, P.G.; Endler, M. Middlewares e protocolos para redes sociais pervasivas. 17 p. Eng.

[2] Facebook Statistics: http://facebook.com/press/info.php?statistics

[3] M. Endler, A. Skyrme, T. Schuster, T. Springer, Defining Situated Social Context for Pervasive Social Computing, Proc. of the 2nd Workshop on Pervasive Collaboration and Social Networking (PerCol 2011), adjunct proceedings of  IEEE Percom 2011, Seattle, March 2011

[4] Google, Inc., "OpenSocial - Google Code", http://code.google.com/apis/opensocial, 2010.

[5] http://code.google.com/apis/maps/documentation/directions/