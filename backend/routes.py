"""Application routes."""
from datetime import datetime as dt

from flask import current_app as app
from flask import make_response, redirect, render_template, request, url_for
from sqlalchemy import desc
from flask import jsonify
from .models import Item, Price, Transaction, db

@app.route("/api/summary", methods=["GET"])
def get_sumarry():
    data = []
    result = Item.query.all()
    for item in result:

        price = Price.query.filter(Price.item_id == item.id).order_by(desc(Price.timestamp)).limit(2).all()
        if len(price) > 1:
            entry = {}
            priceNew = {}
            priceOld = {}

            entry['name'] = item.name
            
            priceNew['timestamp'] = price[0].timestamp.strftime("%Y-%m-%d %H:%M:%S")
            priceNew['price'] = price[0].price

            priceOld['timestamp'] = price[1].timestamp
            priceOld['price'] = price[1].price
            
            entry['priceNew'] = priceNew
            entry['priceOld'] = priceOld

            entry['priceChange'] = priceNew['price'] - priceOld['price']
            entry['priceChangeProc'] = entry['priceChange'] / priceOld['price'] * 100
            

            data.append(entry)

    return jsonify(data)