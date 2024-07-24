from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from Modulos.extract_alternative import extract_alternative
from cachetools import TTLCache
from Modulos.extract_html import extract_data   
from Modulos.api_polygon import polygon
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.models import *
from app.database import get_db
from app.logs import *

app = FastAPI()

cache = TTLCache(maxsize=100, ttl=60)

@app.get("/stock/{company_code}",status_code=status.HTTP_200_OK)
def get_stock(company_code: str,db: Session = Depends(get_db)):
    try:
        logging.info("New Request GET, validating information "+str(company_code))
        load_dotenv()
        json_return = StockJson()
        company_code = company_code.upper()
        if company_code in cache:
            return cache[company_code]
        stock_json,date = polygon(company_code)
        json_return.company_code = company_code
        try:
            logging.info("Trying extraction via MarketWatch")
            extract_json,company_name = extract_data(company_code)
        except:
            logging.info("Trying extraction via MARKETBEAT")
            extract_json,company_name = extract_alternative(company_code)
        json_return.competitors = extract_json["Competitors"]
        json_return.performance_data = extract_json["performance_data"]
        json_return.company_name = company_name
        
        stock = db.query(Stock).filter(Stock.company_code == company_code).first()
        if(stock):
            json_return.purchased_amount = stock.purchased_amount
            json_return.purchased_status = stock.purchased_status
        json_return.status = stock_json.get("status")
        json_return.request_data = date
        json_return.stock_values = StockValues(
            open=stock_json.get('open'),
            high=stock_json.get('high'),
            low=stock_json.get('low'),
            close=stock_json.get('close')
        )
        logging.info("Data returned successfully")
        return json_return
 
    except Exception as error:
        logging.error(str(error.detail))
        if(error.detail=='Error fetching stock data'):
            raise HTTPException(status_code=404, detail=str(error))
        else:
            raise HTTPException(status_code=500, detail=str(error))

@app.post("/stock/{company_code}", status_code=status.HTTP_201_CREATED)
def update_stock(company_code: str, stock_update: StockUpdate, db: Session = Depends(get_db)):
    logging.info("New Request POST, validating information")
    amount = stock_update.amount
    company_code=company_code.upper()
    if not amount:
        logging.error("Amount is required")
        raise HTTPException(status_code=400, detail="Amount is required")
    json_stock = get_stock(company_code,db)
    stock = db.query(Stock).filter(Stock.company_code == company_code).first()    
    if stock:
        stock.purchased_amount += amount
    else:
        stock = Stock(
            company_code=json_stock.company_code,
            purchased_amount=amount,
            status=json_stock.status,
            purchased_status="purchased",
            request_data=json_stock.request_data,
            company_name=json_stock.company_name,
            stock_values={
                "open": json_stock.stock_values.open,
                "high": json_stock.stock_values.high,
                "low": json_stock.stock_values.low,
                "close": json_stock.stock_values.close
            },
            performance_data=json_stock.performance_data ,
            competitors=json_stock.competitors
        )
        db.add(stock)

    db.commit()
    logging.info("Data stored successfully")
    db.refresh(stock)
    return {"message": f"{amount} units of stock {company_code} were added to your stock record"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    if "POST" in request.method:
        logging.error("Amount is required")
        return JSONResponse(
            status_code=400,
            content={"detail": "Amount is required"}
        )