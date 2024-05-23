import requests
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from scipy.signal import savgol_filter
import traceback
from selenium.common.exceptions import TimeoutException

API_KEY = os.environ.get("API_KEY")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

# Função de login
def login(S, _username, _password):
    try:
        S.get("https://twitter.com/i/flow/login")
        print("Starting Twitter")

        # USERNAME
        username_input = WebDriverWait(S, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='text'][class*='r-30o5oe']")))
        username_input.send_keys(_username)
        username_input.send_keys(Keys.ENTER)

        # FIRST BUTTON
        button1 = WebDriverWait(S, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.css-1qaijid.r-bcqeeo.r-qvutc0.r-poiln3")))
        button1.click()
        print("button click")

        # PASSWORD
        password_input = WebDriverWait(S, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
        password_input.send_keys(_password)
        password_input.send_keys(Keys.ENTER)
        print("password done")

        # LOGIN BUTTON
        login_button = WebDriverWait(S, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')))
        login_button.click()
        print("login done")

        return True

    except TimeoutException as te:
        print(f"TimeoutException: {te}")
        print("Error details:", traceback.format_exc())
        print("Error during login")
        return False

    except Exception as e:
        print(f"Exception during login: {str(e)}")
        print("Error details:", traceback.format_exc())
        print("Error during login")
        return False

# Função para postar um tweet
def make_a_tweet(S, text, image_path):
    try:
        S.get("https://twitter.com/compose/tweet")
        sleep(10)

        element = WebDriverWait(S, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')))

        textbox = S.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
        textbox.click()
        sleep(5)
        textbox.send_keys(text)

        # Upload da imagem
        upload = S.find_element(By.CSS_SELECTOR, "input[type='file'][data-testid='fileInput']")
        upload.send_keys(image_path)

        sleep(5)

        element = WebDriverWait(S, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))

        wait = WebDriverWait(S, 10)
        target_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]')))
        S.execute_script("arguments[0].scrollIntoView();", target_element)
        target_element.click()

        print("Tweet done")
    except Exception as e:
        print(f"Error during tweet: {str(e)}")

# Inicializar o navegador
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

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Abrir a URL e buscar os dados
url = 'https://www.wunderground.com/history/daily/br/s%C3%A3o-paulo/SBSP'
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
df['Temperature'] = (df['Temperature'] - 32) * 5 / 9

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

# Cria um gráfico de linha suavizado
plt.plot(df_avg['Hour'], df_avg['Temperature_smooth'], marker='o', label='Suavizado')
plt.title(f'Variação da Temperatura em São Paulo {data}')
plt.xlabel('Hora do Dia')
plt.ylabel('Temperatura Média (°C)')
plt.grid(True)
plt.xticks(range(df['Hour'].min(), df['Hour'].max() + 1))  # Define as legendas para cada hora do dia com base nos dados
plt.tight_layout()

# Salva o gráfico
plt.savefig("temp_sp.png", dpi=300, bbox_inches='tight')

# Fecha o navegador
driver.quit()

print("Gráfico gerado com sucesso")

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
    
    # Reabrir o navegador para postar o tweet
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    if login(driver, username, password):
        # Postando o tweet com a imagem
        make_a_tweet(driver, temp_now, "temp_sp.png")
    else:
        print("Erro ao fazer login no Twitter")

except Exception as e:
    print(f'Deu ruim o twitter: {e}')
    pass

# Fecha o navegador
driver.quit()
