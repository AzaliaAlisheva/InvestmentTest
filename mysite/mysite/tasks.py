from django.forms.models import model_to_dict
import requests
from .models import Stocks
from celery import shared_task

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
    stocks=[]
    for st in views.data:
        get_data(event.data[st]['name'], stocks)
    async_to_sync