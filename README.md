# Botoronga

Este repositório contém dois scripts em execução no GitHub Actions para fornecer informações sobre o clima de São Paulo e os tópicos em alta do Reddit, postando ambas informações de hora em hora no Twitter.

## rilclima.py

Este script é responsável por obter dados de temperatura históricos e atuais de São Paulo. Ele utiliza Selenium e pandas para extrair dados de temperatura de um site meteorológico e OpenWeatherMap API para obter a temperatura atual. Em seguida, ele gera um gráfico da variação da temperatura ao longo do dia e posta a temperatura atual no Twitter.

## bototrend.py (função desligada no momento)

Este script obtém o tópico em alta do Reddit e o publica no Twitter. Ele utiliza a API do Reddit (PRAW) para acessar os tópicos em alta de subreddits aleatórios e escolhe um tópico para postar no Twitter.

Ambos os scripts são executados regularmente no GitHub Actions para manter as informações atualizadas no perfil do Twitter associado.

### Onde posso encontrar?
Pode ser encontrado em [Botoronga](https://twitter.com/botoronga2).

---
**Nota:** Os detalhes de autenticação e configuração dos scripts foram omitidos por motivos de segurança. Certifique-se de configurar corretamente as credenciais e tokens de acesso no script auth.py ou pelo Github Secrets antes de executar os scripts.
