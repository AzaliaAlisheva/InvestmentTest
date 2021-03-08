from django.shortcuts import render
import requests

def get_pc(symbol):
    url = "https://finnhub.io/api/v1/quote?symbol={}&token=sandbox_c0t96iv48v6r4maen2gg"
    r = requests.get(url.format(symbol)).json()
    return r['pc']

def index(request):
    list_of_stocks = ['AAPL', 'AMZN', 'GME', 'TSLA']
    context = {'list': list_of_stocks, 'tableHeader': ['name', 'price', 'chng', 'chng%']}
    return render(request, 'layout.html', context)
