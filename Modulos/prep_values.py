from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

def convert_float(value):
    try:
        formats = {
            'K':10**3,
            'M': 10**6,
            'B': 10**9,
            'T': 10**12

        }
        value_num = float(value[:-1])
        format = value[-1]
        num_float = value_num * formats.get(format,1)
    except:
        num_float = float(value)
    return num_float

def regex_value_format(valor:str):
    regex = r'^([^\d]+)([\d.,]+[A-Z]*)'

    valor = re.match(regex,valor)
    if(valor)==None:        
        valor = ["","",0.0]         

    return valor

def get_last_weekday(current_date:datetime):

    # Data atual
    current_date = current_date - timedelta(days=1)
    while current_date.weekday() >= 5:  # 5 para sábado, 6 para domingo
        current_date -= timedelta(days=1)  # Voltar um dia
    last_weekday = current_date.strftime('%Y-%m-%d')

    return last_weekday