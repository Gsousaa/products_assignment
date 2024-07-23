import requests
import os
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime, timedelta
from .prep_values import *


    # Função para calcular o desempenho
def calculate_performance(start_date:str, end_date:str,symbol:str):
    # Obter dados históricos
    ticker = yf.Ticker(symbol)

    data = ticker.history(start=start_date, end=end_date)
    # Calcular a performance
    if not data.empty:
        start_price = data.iloc[0]['Close']
        end_price = data.iloc[-1]['Close']
        performance = (end_price - start_price) / start_price * 100
        return round(float(performance), 2)
    return None

def extract_alternative(symbol:str):

    # URL da página com a lista de concorrentes
    try:
        url = os.getenv("URL_MARKETBEAT_NASDAQ").replace("{symbol}",symbol)

        # Fazer a requisição para o site
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tabela com os concorrentes
        table = soup.find('table', {'id': 'competitors-table'})    
        titulo = soup.find('h1', {'id':'pageTitle'}).text.replace("\n","").replace(" Competitors","")
            # Verificar se a tabela foi encontrada
        if not table:
            raise Exception("Tabela de competidores não encontrada na página.")           
    except:
        url = os.getenv("URL_MARKETBEAT_NYSE").replace("{symbol}",symbol)

        # Fazer a requisição para o site
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tabela com os concorrentes
        table = soup.find('table', {'id': 'competitors-table'})
        titulo = soup.find('h1', {'id':'pageTitle'}).text.replace("\n","").replace(" Competitors","")    

        

    # Extrair os símbolos dos concorrentes
    list_competitors = []
    for tr in table.find_all('tr')[1:]:  # Pular o cabeçalho
        td = tr.find_all('td')
        if len(td) > 0:
            value = regex_value_format(td[5].text.strip())
            list_competitors.append({
                "name": td[0].attrs.get('data-clean').split("|")[0],
                "market_cap": {
                    "Currency": str(value[1]),
                    "Value": convert_float(value[2])
                }
            })

    # Data de hoje
    today = datetime.now()

    # Calcular as datas de início para cada período
    five_days_ago = today - timedelta(days=5)
    one_month_ago = today - timedelta(days=30)
    three_months_ago = today - timedelta(days=90)
    one_year_ago = today - timedelta(days=365)
    ytd_start = datetime(today.year, 1, 1)

    # Calcular a performance para cada período
    performance = {
        'five_days': float(calculate_performance(five_days_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),symbol)),
        'one_month': float(calculate_performance(one_month_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),symbol)),
        'three_months': float(calculate_performance(three_months_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),symbol)),
        'year_to_date': float(calculate_performance(ytd_start.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),symbol)),
        'one_year': float(calculate_performance(one_year_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),symbol))
    }
    
    return_json = {
    "performance_data": performance,
    "Competitors": list_competitors
    }
    #print(return_json)
    return return_json,titulo
