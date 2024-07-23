from fastapi import FastAPI, HTTPException
from Modulos.extract_alternative import extract_alternative
from cachetools import TTLCache
from Modulos.extract_html import extract_data   
from Modulos.api_polygon import polygon
from dotenv import load_dotenv

app = FastAPI()

# Configurar o cache com TTL de 60 segundos e máximo de 100 entradas
cache = TTLCache(maxsize=100, ttl=60)


@app.get("/stock/{company_code}")
def get_stock(company_code: str):
    try:
        load_dotenv()
        company_code = company_code.upper()
        if company_code in cache:
            return cache[company_code]
        
        try:
            extract_json,company_name = extract_data(company_code)
        except:
            extract_json,company_name = extract_alternative(company_code)
        stock_json,date = polygon(company_code)
        
        final_result = {
            "Status": "Success",
            "purchased_amount": 0, 
            "purchased_status": "Waiting Purchase",  
            "request_data": date,
            "company_code": company_code,
            "company_name": company_name, 
            "Stock_values": {
                "open": stock_json.get('open'),
                "high": stock_json.get('high'),
                "low": stock_json.get('low'),
                "close": stock_json.get('close')
            },
            "performance_data": extract_json["performance_data"],
            "Competitors": extract_json["Competitors"]        
        }
        
        return final_result
 
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
#get_stock("meta")