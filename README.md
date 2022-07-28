# coronga2.0
Bot em Python para postar informações sobre o COVID-19 no Twitter 

Essa daqui é uma nova versão do https://github.com/Rilufi/coronga , todas as informações adicionais se encontram lá, então vou citar somente as diferenças principais.

## dados COVID
Todos os dados sobre o COVID-19 estão sendo retirados da planilha atualizada diariamente de https://covid.ourworldindata.org sem necessidade de pacotes de terceiros.

## Por que outro repositório praticamente igual???
Não, eu não estou querendo só encher linguiça no github, é que além da outra fonte de dados que eu usava não funcionar mais, eu adicionei essa resposta com mais info e que não dependa de pacotes extras pra rodar, só pega diretamente os dados de uma planilha csv pelo pandas.

## Gráficos
Agora também temos gráficos! O script que faz os gráficos é o covidson.py, coloquei um workflow agendado pra rodar todo dia e já autocomitar os gráficos atualizados no repositório, esse workflow já ativa o próximo que roda o script botoronga.py que pega os gráficos pra postar junto dos dados diretos, tudo em sequência usando o último tweet como base.

## Onde está o bot?
Só entrar aqui pra encontrar o resultado: [Botoronga](https://twitter.com/botoronga)
