import requests
from auth import API_KEY, client, api
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.utils import ChromeType
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep, time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

url = 'https://www.wunderground.com/history/daily/br/s%C3%A3o-paulo/SBSP'
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get(url)

# Aguarda a presença das tabelas na página
tables = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table")))

# Cria um DataFrame vazio para armazenar os dados
df = pd.DataFrame(columns=['Time', 'Temperature'])

for table in tables:
    # Lê a tabela HTML usando pandas
    new_table = pd.read_html(table.get_attribute('outerHTML'))

    if new_table:
        # Algumas tabelas podem ter colunas adicionais ou informações extras
        # Neste caso, estamos interessados nas colunas 'Time' e 'Temperature'
        if 'Time' in new_table[0].columns and 'Temperature' in new_table[0].columns:
            # Adiciona os dados relevantes ao DataFrame
            df = pd.concat([df, new_table[0][['Time', 'Temperature']].fillna('')], ignore_index=True)

# Lida com valores nulos na coluna 'Time' e substitui por uma string vazia
df['Time'].fillna('', inplace=True)

# Converte o formato AM/PM para 24 horas, tratando os valores vazios
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').dt.strftime('%H:%M')

# Extrai apenas os números da temperatura, tratando os valores vazios
df['Temperature'] = df['Temperature'].str.extract('(\d+)', expand=False).astype(float)

# Remove as linhas com valores nulos resultantes da conversão
df.dropna(subset=['Time'], inplace=True)

# Converte a temperatura de Fahrenheit para Celsius
df['Temperature'] = (df['Temperature'] - 32) * 5/9

# Arredonda as temperaturas para no máximo duas casas decimais
df['Temperature'] = df['Temperature'].round(2)

# Salva os dados em um arquivo CSV
df.to_csv('clima_sp_data.csv', index=False)

# Cria um gráfico de linha
data = date.today().strftime('%d/%m/%Y')
plt.plot(df['Time'], df['Temperature'], marker='o')
plt.title(f'Variação da Temperatura em São Paulo {data}')
plt.xlabel('Hora do Dia')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Mostra o gráfico
plt.savefig("temp_sp")
#plt.show()

# Fecha o navegador
driver.quit()

print("Dados salvos com sucesso em 'clima_sp_data.csv' e gráfico gerado.")


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
    #client.create_tweet(text=temp_now)
    media = api.media_upload("temp_sp.png")
    client.create_tweet(text=temp_now, media_ids=[media.media_id])
except:
    pass
