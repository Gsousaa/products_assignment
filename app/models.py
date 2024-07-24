from sqlalchemy import Column, Integer, String, Float, Date, JSON
from .database import Base, engine
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from typing import List, Dict, Any


class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    company_code = Column(String, index=True)
    status = Column(String)
    purchased_amount = Column(Float) 
    purchased_status = Column(String)
    request_data = Column(Date)    
    company_name = Column(String)
    stock_values = Column(JSON)
    performance_data = Column(JSON)
    competitors = Column(JSON)

Base.metadata.create_all(bind=engine)

class StockUpdate(BaseModel):
    amount: float

class MarketCap(BaseModel):
    currency: Optional[str] = None
    value: Optional[float] = None

class Competitor(BaseModel):
    name: Optional[str] = None
    market_cap: Optional[MarketCap] = None

class StockValues(BaseModel):
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None

class PerformanceData(BaseModel):
    five_days: Optional[float] = None
    one_month: Optional[float] = None
    three_months: Optional[float] = None
    year_to_date: Optional[float] = None
    one_year: Optional[float] = None

class StockJson(BaseModel):
    status: Optional[str] = None
    purchased_amount: Optional[int] = None
    purchased_status: Optional[str] = None
    request_data: Optional[str] = None
    company_code: Optional[str] = None
    company_name: Optional[str] = None
    stock_values: Optional[StockValues] = None
    performance_data: Optional[PerformanceData] = None
    competitors: Optional[List[Competitor]] = None