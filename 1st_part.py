# All Brazilian Mall Data in Excel - Web Scrapping using Python - Free and Open Sample
# Developed by: Leonardo T. Delboni (Feb/2025)

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URLs de shoppings
list_url = [
    'https://abrasce.com.br/guia-de-shoppings/',
    'https://abrasce.com.br/guia-de-shoppings/page/2/',
    'https://abrasce.com.br/guia-de-shoppings/page/3/',
    'https://abrasce.com.br/guia-de-shoppings/page/4/',
    'https://abrasce.com.br/guia-de-shoppings/page/5/',
    'https://abrasce.com.br/guia-de-shoppings/page/6/',
    'https://abrasce.com.br/guia-de-shoppings/page/7/'
]

# Lista para armazenar os dados dos shoppings
shopping_data = []
aux = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # Para cada URL na lista de URLs, extrair os dados
    print('\n\n Iniciando a coleta de dados:')
    for url in list_url:
        print('\n\nColetando dados de:', url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        print('Status:', response.status_code)	
        print('Código fonte:', soup.prettify())
        
        # Encontrar todos os elementos de shopping
        shoppings = soup.find_all('div', class_='shopping')
        
        for shopping in shoppings:
            name_div = shopping.find('div', class_='col-12')
            state_div = shopping.find('div', class_='footer')
            shopping_url = shopping.find('a')['href'] if shopping.find('a') else None
            
            if name_div and state_div and shopping_url:
                name = name_div.text.strip()
                state = state_div.text.strip()
                
                # Adicionar os dados à lista
                shopping_data.append({
                    'Nome': name,
                    'Estado': state,
                    'URL': shopping_url
                })

                print('\n\n Dados coletados:')
                print('Número:', aux)
                print('Dados coletados:', name)
                print('Estado:', state)
                print('URL:', shopping_url)
                aux += 1

    # Criar um DataFrame do pandas com os dados coletados
    df = pd.DataFrame(shopping_data)
    print('\n\n Dataframe final:')
    print(df)

    # Salvar os dados em um arquivo Excel
    print('\n\n Salvando em Excel:')
    df.to_excel('shoppings.xlsx', index=False)

except Exception as e:
    print('Erro:', e)
    print('Erro ao coletar dados dos shoppings. Programa encerrado.')
    exit()
