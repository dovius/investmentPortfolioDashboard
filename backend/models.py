"""Data models."""
from . import db
import datetime

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    xpath = db.Column(db.String)
    prices = db.relationship("Price", backref=db.backref("item"))
    transactions = db.relationship("Transaction", backref=db.backref("item"))
    
class Price(db.Model):
    __tablename__ = "price"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Float)

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))
    timestamp = db.Column(db.Time)
    action = db.Column(db.String)
    type = db.Column(db.String)
    platform = db.Column(db.String)
    url = db.Column(db.String)
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    sum = db.Column(db.Float)