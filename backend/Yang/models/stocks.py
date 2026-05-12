# 202501552/models/stock.py

from sqlalchemy import Column, Integer, String, Float
from db.session import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    date = Column(String)
    close = Column(Float)