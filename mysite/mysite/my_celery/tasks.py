from django.forms.models import model_to_dict
import requests
from celery import shared_task
import datetime
import time
from django.apps import apps
from .scraper import StockTickerScraper

def_ticker = 'AAPL'
def_service = 'finnhub'

@shared_task
def perform_scrape(ticker=def_ticker, service=def_service):
    client = StockTickerScraper(service=service)
    pc = client.scrape(ticker=ticker)
    print('task', ticker, pc)
    PriceLookupEvent = apps.get_model("mysite", "PriceLookupEvent")
    PriceLookupEvent.objects.create_event(ticker, pc, source=service)


@shared_task
def company_price_scrape_task(instance_id, service=def_service):
    Stock = apps.get_model("mysite", "Stock")
    obj = Stock.objects.get(id=instance_id)
    ticker = obj.ticker
    perform_scrape(ticker=ticker, service=service)


@shared_task
def company_granular_price_scrape_task(instance_id, service=def_service):
    Stock = apps.get_model("mysite", "Stock")
    obj = Stock.objects.get(id=instance_id)
    print("hi")
    ticker = obj.ticker
    perform_scrape(ticker=ticker, service=service)
    if obj.has_granular_scraping:
        now = datetime.datetime.now()
        expires = now + datetime.timedelta(seconds=65)
        for i in range(1, 60):  # 1 - 59
            perform_scrape.apply_async(kwargs={
                "ticker": ticker,
                "service": service
            }, countdown=i, expires=expires)

"""
def get_data(symbol, stocks):
    url = "https://finnhub.io/api/v1/quote?symbol={}&token=sandbox_c0t96iv48v6r4maen2gg"
    r = requests.get(url.format(symbol)).json()
    obj, created = Stocks.object.get_or_create(symbol=symbol)
    obj.name = symbol
    obj.pc = r['pc']
    obj.save()
    new_data = model_to_dict(obj)
    new_data.update({'state': state})
    stocks.append(new_data)

@shared_task
def get_stocks_data():
    for st in AllStocks:
        get_data(event.data[st]['name'], stocks)
    async_to_sync"""