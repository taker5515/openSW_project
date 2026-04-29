# 202501552/main.py

from fastapi import FastAPI
from api.routes import stock
from db.session import engine
from models import stock as stock_model

app = FastAPI()

stock_model.Base.metadata.create_all(bind=engine)

app.include_router(stock.router)