from models import Item, Price, Transaction
from base import session_factory
import pandas
from lxml import html
import requests
import re
from datetime import datetime
from sqlalchemy import desc
import json

session = session_factory()

def importItems():
    print('import')
    items = pandas.read_csv('../data/items.csv')
    for item in items.itertuples():
        session.add(Item(name=item.name, xpath=item.xpath, url=item.url))
    session.commit()

def getAllItems():
    print('getall')
    items_query = session.query(Item)
    return items_query.all()

def extractPrice(priceString):
    print('---> extractPrice')
    price = ''.join(priceString)
    price = re.findall(r"[-+]?\d*\.\d+|\d+", price.replace(',',''))
    print('<--- extractPprice', price[0])
    return float(price[0])

def scanPrice(url, xpath):
    print('--> scanPrice')
    page = requests.get(url)
    tree = html.fromstring(page.content)
    priceString = tree.xpath(xpath)
    price = extractPrice(priceString)
    # f = open("response" + datetime.now().ctime() + ".html", "a")
    # f.write(page.text)
    # f.close()
    print('<-- scanPrice')
    return price

def importHistory():
    page = requests.get("https://markets.ft.com/data/equities/ajax/get-historical-prices?startDate=2021%2F01%2F01&endDate=2021%2F12%2F16&symbol=99144764")
    data = json.loads(page.text)
    f = open("response" + datetime.now().ctime() + ".html", "a")
    f.write(data['html'])
    f.close()
    print(data['html'])


allItems = getAllItems()
if len(allItems) == 0:
    importItems()
    allItems = getAllItems()

for item in allItems:
    print('-> process ' + item.name)
    currentPrice = scanPrice(item.url, item.xpath)
    lastSavedPrice = session.query(Price).filter(Price.item_id == item.id).order_by(desc(Price.timestamp)).first()

    if lastSavedPrice is None or lastSavedPrice.price != currentPrice:
        print('-> add price')
        session.add(Price(item=item, price=currentPrice))

session.commit()
