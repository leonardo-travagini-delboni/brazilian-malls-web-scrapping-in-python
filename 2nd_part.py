# All Brazilian Mall Data in Excel - Web Scrapping using Python - Free and Open Sample
# Developed by: Leonardo T. Delboni (Feb/2025)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do Selenium usando WebDriver Manager
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rodar sem abrir o navegador (opcional)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Inicializa o driver do Chrome automaticamente com a versão correta
service = Service(ChromeDriverManager().install())  
driver = webdriver.Chrome(service=service, options=chrome_options)

# Tempo máximo de espera para carregamento dinâmico
wait = WebDriverWait(driver, 10)

# Carregar o Excel com as URLs
df = pd.read_excel("shoppings.xlsx")

# Excel auxiliar para cada iteração
excel_aux="shoppings_aux.xlsx"

# Lista para armazenar os dados extraídos
dados_extraidos = []

# Função para extrair informações do HTML
def extrair_dados(url):
    driver.get(url)
    
    # Espera extra para garantir que os dados dinâmicos sejam carregados
    time.sleep(4)

    def get_text_safe(xpath):
        try:
            elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            texto = elemento.text.strip()
            return texto if texto else "Não encontrado"
        except:
            return "Não encontrado"

    # Dicionário com os dados extraídos
    dados = {
        "URL": url,
        "ADMINISTRADORA": get_text_safe('//*[@id="mfs_administradora"]'),
        "ENTRETENIMENTO": get_text_safe('//*[@id="mfs_entretenimento"]'),
        "ÁREA_TOTAL_TERRENO": get_text_safe('//*[@id="mfs_total"]'),
        "ÁREA_CONSTRUIDA": get_text_safe('//*[@id="mfs_contruida"]'),
        "ÁREA_BRUTA_LOCAVEL": get_text_safe('//*[@id="mfs_bruta"]'),
        "TELEFONE": get_text_safe('//*[@id="mfs_fone"]'),
        "SITE": get_text_safe('//*[@id="mfs_site"]'),
        "ENDEREÇO": get_text_safe('//*[@id="mfs_endereco"]')
    }
    
    return dados

# Percorre todas as URLs e coleta os dados
aux = 1
for url in df["URL"]:
    print(f"\n\nColetando dados do shopping {aux} de {len(df)}...")
    print(f"Extraindo dados de: {url}")
    dados = extrair_dados(url)
    dados_extraidos.append(dados)
    print(dados)
    print('Dados extraídos:', dados_extraidos)

    # Adicionando os dados ao final do Excel auxiliar
    print("Salvando dados no Excel auxiliar...")
    df_aux = pd.read_excel(excel_aux)
    df_iteracao = pd.DataFrame([dados])
    df_aux = pd.concat([df_aux, df_iteracao], ignore_index=True)
    df_aux.to_excel(excel_aux, index=False)
    aux += 1

# Fecha o navegador ao finalizar
driver.quit()

# Criar DataFrame com os dados coletados
df_extraidos = pd.DataFrame(dados_extraidos)

# Salvar os resultados em um novo Excel
df_extraidos.to_excel("shoppings_dados.xlsx", index=False)
print("✅ Extração concluída! Dados salvos em 'shoppings_dados.xlsx'.")
