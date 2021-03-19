# coronga2.0
Bot em Python para postar informações sobre o COVID-19 no Twitter 

Essa daqui é uma nova versão do https://github.com/Rilufi/coronga , todas as informações adicionais se encontram lá, então vou citar somente as diferenças principais.

## dados COVID
Para os dados do Brasil: https://pypi.org/project/covid/
Para os dados dos EUA e do mundo: https://pypi.org/project/COVID19Py/

## Mortes 24h
Adicionei um "Mortes em 24h" que funciona atualizando todo dia um csv que contém o número de mortos do dia anterior, então troque o número embaixo de "Mortos" com os dados do dia, que a partir do próximo dia ele fará isso automaticamente.

## Tweets
Ele agora tweeta a primeira info e responde pra ele mesmo a segunda info em seguida, só precisa falar o user, substituindo o @ do usuário onde está toReply = "user"

## Failsafe
Como as vezes o repositório para os EUA e pro mundo não funciona direito por algum problema de permissão do API do heroku, mas o outro repositório também só tem infos do Brasil, eu coloquei um failsafe em que ele posta do Brasil e tenta postar dos EUA e pro mundo, se não conseguir fica só com Brasil.

## Por que outro repositório praticamente igual???
Não, eu não estou querendo só encher linguiça no github, é que além da outra fonte de dados que eu usava não funcionar mais no pythonanywhere, eu adicionei essa resposta com mais info, mas como o outro repositório ainda funciona, não fazia sentido eu apenas substituir lá.
