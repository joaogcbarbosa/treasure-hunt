- Servidor: é inicializado com host e porta. Fica escutando e aceitando as solicitações de conexão de novos clientes. Quando o número de conexões passa a ser igual ao número de players informados para a partida, o servidor "spawna" os jogadores no mapa principal e aguarda em looping infinito até a condição da flag de parada ser verdadeira, momento de encerramento da thread do servidor.

- Clientes: duas ou três threads que ficam em looping infinito executando a função "play" (se movendo pelos mapas e coletando pontos) até que a condição de parada seja verdadeira (ambos mapas com nenhum ponto restante para ser coletado).

1) game_map e special_game_map: são, respectivamente, o mapa principal e o mapa especial. São as regiões críticas do jogo e são protegidos por map_semaphore e special_map_semaphore, nessa ordem.

2) special_map_queue: é a fila que gerencia a entrada no mapa especial. Tem tamanho máximo variável: se for escolhido que no jogo terão dois players, a fila terá tamanho um, se for escolhido que no jogo terão três players, a fila terá tamanho dois. Ou seja, a fila sempre terá tamanho (MAX_PLAYERS - 1), visto que o primeiro que tentar entrar no mapa não precisa entrar em fila, pois antes é checado se o semáforo do mapa especial tem valor 1 ou 0. Se for 0 entra para fila, se for 1 acessa direto o mapa especial.

3) map_semaphore: não deixa que a thread de cada player faça a visualização de como está a situação do mapa principal (pois se a visualização não estiver protegida pelo semáforo pode ser que quando o jogador for se movimentar a situaçã do mapa já seja outra) e realize a movimentação simultaneamente com outras threads. Também protege a lógica que envia o jogador que estava no mapa especial de volta para o mapa principal: a lógica pega a primeira posição livre que acha no mapa principal e dá para o jogador que está voltando. Portanto, é necessário que no mapa principal não esteja havendo movimento de outros players, evitando que duas threads acabem, aleatoriamente, pegando a mesma posição.

4) special_map_semaphore: não tem o mesmo objetivo de proteger diretamente o mapa, assim como o map_semaphore, mas sim de sinalizar se a thread do player deve ir pra uma fila de espera ou acessar diretamente o mapa especial, a depender do valor de special_map_semaphore. Se já tiver um jogador no mapa especial, então possíveis jogadores que também tentarem entrar passam para uma espera ocupada, liberando o semáforo do mapa principal, deixando de se mover no mapa principal e apenas esperando pela vez de entrar no mapa especial.

5) check_semaphore: este é um semáforo suporte. Serve para uma thread, que está na fila, de cada vez checar se o mapa especial está liberado ou não (valor 1 ou 0). 


- Cada vez que rodar o main.py, excluir o log gerado na raiz, pois está no modo append. Caso não seja excluído, as informações de diferentes execuções ficarão uma em cima da outra;
- Foi usado o Python 3.12.0 para o desenvolvimento (environment.yml);
- As dependências listadas no pyproject.toml foram apenas para desenvolvimento (formatação do código).