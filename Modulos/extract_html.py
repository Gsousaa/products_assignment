import re
import os
import requests
from bs4 import BeautifulSoup
from .prep_values import *


def extract_performance(soup:str):
    performance_div = soup.find('div', class_='element element--table performance')
    list_performance = str(performance_div).split('<li class="content__item value ignore-color">')
    performance_data = {
    "five_days": float(re.search(r"[-+]?\d*\.\d", list_performance[1])[0]),
    "one_month": float(re.search(r"[-+]?\d*\.\d", list_performance[2])[0]),
    "three_months": float(re.search(r"[-+]?\d*\.\d", list_performance[3])[0]),
    "year_to_date": float(re.search(r"[-+]?\d*\.\d", list_performance[4])[0]),
    "one_year": float(re.search(r"[-+]?\d*\.\d", list_performance[5])[0])
}
    return performance_data

def extract_competitors(soup:str):
    performance_div = soup.find('div', class_='element element--table overflow--table Competitors')
    list_competitors = []
    competitors = performance_div.find_all('tr', class_='table__row')[1:]
    for competitor in competitors:
        competitor = competitor.text.split("\n")

        value = regex_value_format(competitor[3])    
        list_competitors.append({
            "name": str(competitor[1]),
            "market_cap": {
                "Currency": str(value[1]),
                "Value": convert_float(value[2])
            }
        })
    
    return list_competitors

def extract_data(company_code:str):

    url = os.getenv("URL_MARKETWATCH")+'/'+company_code

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com.br/"
        }

    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    performance_data = extract_performance(soup)
    company_name = soup.find('h1', {'class':'company__name'}).text

    competitors = extract_competitors(soup)
    return_json = {
    "performance_data": performance_data,
    "Competitors": competitors
    }

    return return_json, company_name
