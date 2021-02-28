from django.shortcuts import render
import requests


def index(request):
    """url = "https://finnhub.io/api/v1/quote?symbol={}&token=sandbox_c0t96iv48v6r4maen2gg"
    symbol = 'AMZN'
    r = requests.get(url.format(symbol)).json()
    quote = {
        'symbol': symbol,
        'price': r['c'],
        'chng': (r['c']-r['pc']),
        'chng%': (r['c']-r['pc'])*100/r['pc'],
    }
    print(quote, r['o'])"""
    return render(request, 'layout.html')
