from django.shortcuts import render
import requests


def index(request):
    url = "https://finnhub.io/api/v1/quote?symbol=AAPL&token=sandbox_c0t96iv48v6r4maen2gg"
    r = requests.get(url)
    print(r.text)
    return render(request, 'layout.html')