import random
from auth import client, api


# Dicionário contendo os grupos de tweets e suas respectivas imagens
tweets_e_imagens = {
    'Texto1': {
        'tweets': [
            "Ajude o RS em sua calamidade pública. Faça sua doação via Pix para a conta SOS Rio Grande do Sul (CNPJ: 92.958.800/0001-38). Sua contribuição é auditada para transparência total. #SOSRioGrandeDoSul",
            "O RS precisa de nós! Doe para SOS Rio Grande do Sul via Pix (CNPJ: 92.958.800/0001-38). Ajuda centralizada e segura. #SOSRioGrandeDoSul",
            "Contribua com as vítimas das enchentes no RS. Pix: SOS Rio Grande do Sul, CNPJ 92.958.800/0001-38. Cada doação faz a diferença! #SOSRioGrandeDoSul",
            "Seu apoio é vital para o RS. Doações via Pix para SOS Rio Grande do Sul (CNPJ: 92.958.800/0001-38) ajudam diretamente quem precisa. #SOSRioGrandeDoSul",
            "Solidariedade com o RS. Use o Pix (CNPJ: 92.958.800/0001-38) para doar para a conta SOS Rio Grande do Sul. Transparência garantida. #SOSRioGrandeDoSul"
        ],
        'imagem': 'imagem_texto1.png'
    },
    'Texto2': {
        'tweets': [
            "Os times gaúchos estão unidos pelas vítimas das chuvas. Doe via Pix para o Grêmio (CNPJ: 129859670001-59). Internacional e Juventude recebem doações físicas. #SOSRioGrandeDoSul",
            "Ajude o RS com o Grêmio pelo Pix (CNPJ: 129859670001-59). Internacional e Juventude coletam itens essenciais. #SOSRioGrandeDoSul",
            "Solidariedade em campo! Grêmio, Internacional e Juventude mobilizados para ajudar o RS. Doe via Pix (CNPJ: 129859670001-59). #SOSRioGrandeDoSul",
            "Faça parte da torcida pelo RS! Contribua com o Grêmio via Pix (CNPJ: 129859670001-59) ou doe itens no Internacional e Juventude. #SOSRioGrandeDoSul",
            "Vista a camisa da ajuda! Doe para o Grêmio via Pix (CNPJ: 129859670001-59) ou traga doações ao Internacional e Juventude. #SOSRioGrandeDoSul"
        ],
        'imagem': 'imagem_texto2.png'
    },
    'Texto3': {
        'tweets': [
            "A prefeitura de São José convoca doações para vítimas das chuvas. Entregue itens essenciais na sede do Procon. #SOSRioGrandeDoSul",
            "Santa Cruz do Sul busca voluntários para ajudar após enchentes. Inscreva-se no site da prefeitura. #SOSRioGrandeDoSul",
            "Taquara precisa de doações! Entregue na Secretaria de Desenvolvimento ou doe via Pix: 51996654645. #SOSRioGrandeDoSul"
        ],
        'imagem': 'imagem_texto3.png'
    },
    'Texto4': {
        'tweets': [
            "O Hemocentro de Porto Alegre alerta para a necessidade urgente de doações de sangue. Agende pelo tel (51) 3339-7330 ou WhatsApp (51) 98405-4260. #SOSRioGrandeDoSul",
            "Ajude a manter o estoque de sangue! O Hemocentro de Porto Alegre está aberto para doações. Mais informações: (51) 3339-7330 ou WhatsApp (51) 98405-4260. #SOSRioGrandeDoSul",
            "Doar sangue salva vidas! Em Porto Alegre, ligue para (51) 3339-7330 ou envie uma mensagem para (51) 98405-4260 e agende sua doação. #SOSRioGrandeDoSul",
            "Porto Alegre precisa de doadores de sangue. Contate o Hemocentro: (51) 3339-7330 ou (51) 98405-4260. Sua ação pode salvar vidas. #SOSRioGrandeDoSul",
            "Seja um herói do cotidiano. Doe sangue no Hemocentro de Porto Alegre. Agendamentos: (51) 3339-7330 / (51) 98405-4260. #SOSRioGrandeDoSul"
        ],
        'imagem': 'imagem_texto4.png'
    },
    'Texto5': {
        'tweets': [
            "Porto Alegre se mobiliza! Doe colchões, roupas de cama, itens de higiene e mais na Defesa Civil. Locais: Amrigs, Shoppings Iguatemi, João Pessoa, Total e outros. #SOSRioGrandeDoSul",
            "Sua ajuda é essencial em Porto Alegre. A Defesa Civil precisa de doações de itens básicos e para pets. Confira os pontos de coleta. #SOSRioGrandeDoSul",
            "Faça a diferença! Contribua com itens de necessidade e para animais nos pontos de coleta da Defesa Civil em Porto Alegre. #SOSRioGrandeDoSul",
            "Ajude as vítimas das chuvas em Porto Alegre. Doações são recebidas na Amrigs, shoppings e estádios. Veja onde contribuir. #SOSRioGrandeDoSul",
            "Defesa Civil de Porto Alegre convoca para doação de itens urgentes. Encontre o ponto de coleta mais próximo e ajude! #SOSRioGrandeDoSul"
        ],
        'imagem': 'imagem_texto5.png'
    }
}

# Função para escolher aleatoriamente um tweet de um grupo e retornar o tweet e a imagem correspondente
def escolher_tweet_e_imagem():
    categoria = random.choice(list(tweets_e_imagens.keys()))
    tweet_selecionado = random.choice(tweets_e_imagens[categoria]['tweets'])
    imagem_correspondente = tweets_e_imagens[categoria]['imagem']
    return tweet_selecionado, imagem_correspondente

# Posta a imagem e tweet escolhido
tweet, imagem = escolher_tweet_e_imagem()
print(f"Tweet selecionado: {tweet}")
print(f"Imagem correspondente: {imagem}")
media = api.media_upload(imagem)
client.create_tweet(text=tweet, media_ids=[media.media_id])

