import requests
from auth import API_KEY, client


# Coordenadas geográficas de São Paulo
latitude = -23.550520
longitude = -46.633308

# URL da API do OpenWeatherMap para obter a temperatura atual
url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}'

try:
    # Fazendo a solicitação HTTP
    response = requests.get(url)
    response.raise_for_status()  # Lança uma exceção para códigos de status HTTP diferentes de 200 OK

    # Tentar decodificar o JSON
    data = response.json()

    # Extraindo a temperatura atual
    temperatura_atual = data['main']['temp']

    # Convertendo a temperatura para Celsius
    temperatura_atual_celsius = temperatura_atual - 273.15

    # Imprimindo a temperatura atual em Celsius
    temp_now = f'Temperatura atual em São Paulo: {temperatura_atual_celsius:.2f}°C'
    api.client.create_tweet(text=temp_now)
except:
    pass
