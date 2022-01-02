from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Float, Time
import datetime

from base import Base

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    xpath = Column(String)
    prices = relationship("Price", backref=backref("item"))
    transactions = relationship("Transaction", backref=backref("item"))
    
class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    price = Column(Float)

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"))
    timestamp = Column(Time)
    action = Column(String)
    type = Column(String)
    platform = Column(String)
    url = Column(String)
    amount = Column(Float)
    price = Column(Float)
    sum = Column(Float)