from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from main import app 
import pytest

client = TestClient(app)

def test_get_stock_sucess():
    company_code = "DDD"
    response = client.get(f'/stock/{company_code}')

    assert response.status_code == 200

def test_get_stock_not_found():
    response = client.get("/stock/INVALID_CODE")

    assert response.status_code == 404
    assert response.json() == {"detail": "404: Error fetching stock data"}

def test_update_stock_missing_amount():
    stock_symbol = "DDD"
    payload = {}
    
    response = client.post(f"/stock/{stock_symbol}", json=payload)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Amount is required"}
