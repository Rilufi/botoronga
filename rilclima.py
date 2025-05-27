import requests
import os
from auth import API_KEY, client, api
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import StringIO
from scipy.signal import savgol_filter
import pytz

# Cria a pasta imagens se não existir
os.makedirs('imagens', exist_ok=True)

# Inicializando o Chrome para Web Scraping
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
    html = table.get_attribute('outerHTML')
    new_table = pd.read_html(StringIO(html))

    if new_table:
        # Algumas tabelas podem ter colunas adicionais ou informações extras
        # Neste caso, estamos interessados nas colunas 'Time' e 'Temperature'
        if 'Time' in new_table[0].columns and 'Temperature' in new_table[0].columns:
            # Adiciona os dados relevantes ao DataFrame
            df = pd.concat([df, new_table[0][['Time', 'Temperature']].fillna('')], ignore_index=True)

# Lida com valores nulos na coluna 'Time' e substitui por uma string vazia
df['Time'] = df['Time'].fillna('')

# Converte o formato AM/PM para 24 horas, tratando os valores vazios
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p', errors='coerce').dt.strftime('%H:%M')

# Extrai apenas os números da temperatura, tratando os valores vazios
df['Temperature'] = df['Temperature'].str.extract(r'(\d+)', expand=False).astype(float)

# Remove as linhas com valores nulos resultantes da conversão
df.dropna(subset=['Time'], inplace=True)

# Converte a temperatura de Fahrenheit para Celsius
df['Temperature'] = (df['Temperature'] - 32) * 5/9

# Arredonda as temperaturas para no máximo duas casas decimais
df['Temperature'] = df['Temperature'].round(2)

# Agrupa os dados por hora e calcula a média
df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
df_avg = df.groupby('Hour')['Temperature'].mean().reset_index()

# Verifica se há pontos de dados suficientes para aplicar o filtro de Savitzky-Golay
if len(df_avg) >= 7:
    # Suavização dos dados usando o filtro de Savitzky-Golay
    window_size = 7
    poly_order = 3
    df_avg['Temperature_smooth'] = savgol_filter(df_avg['Temperature'], window_size, poly_order)
else:
    # Se não houver pontos suficientes, use os dados brutos
    df_avg['Temperature_smooth'] = df_avg['Temperature']

# Define o fuso horário do Brasil
fuso_brasil = pytz.timezone('America/Sao_Paulo')

# Obtém a data e hora atual nos EUA
data_eua = datetime.now()

# Ajusta para o fuso horário do Brasil
data_brasil = data_eua.astimezone(fuso_brasil)

# Formata a data no formato dd/mm/yyyy
data = data_brasil.strftime('%d/%m/%Y')

# Versão em português
plt.figure(figsize=(10, 6))
plt.plot(df_avg['Hour'], df_avg['Temperature_smooth'], marker='o', label='Suavizado')
plt.title(f'Variação da Temperatura em São Paulo {data}')
plt.xlabel('Hora do Dia')
plt.ylabel('Temperatura Média (°C)')
plt.grid(True)
# Corrige o erro convertendo para inteiro e garantindo que temos valores válidos
hour_min = int(df_avg['Hour'].min())
hour_max = int(df_avg['Hour'].max())
plt.xticks(range(hour_min, hour_max + 1))
plt.tight_layout()
plt.savefig(os.path.join('imagens', 'clima_sp.png'), dpi=300, bbox_inches='tight')
plt.close()

# Versão em inglês
plt.figure(figsize=(10, 6))
plt.plot(df_avg['Hour'], df_avg['Temperature_smooth'], marker='o', label='Smoothed')
plt.title(f'Temperature Variation in São Paulo {data}')
plt.xlabel('Time of Day')
plt.ylabel('Average Temperature (°C)')
plt.grid(True)
plt.xticks(range(hour_min, hour_max + 1))
plt.tight_layout()
plt.savefig(os.path.join('imagens', 'weather_sp.png'), dpi=300, bbox_inches='tight')
plt.close()

# Fecha o navegador
driver.quit()

print("Gráficos gerados com sucesso")

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
    media = api.media_upload(os.path.join('imagens', 'clima_sp.png'))
    client.create_tweet(text=temp_now, media_ids=[media.media_id])

except Exception as e:
    print(f'Erro ao postar no Twitter: {e}')
