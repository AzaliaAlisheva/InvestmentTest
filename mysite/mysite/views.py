from django.shortcuts import render
from django.views import generic
from .models import Stock


def index(request):
    data = {}
    for stock in Stock.objects.all():
        data[stock.ticker] = {'name': stock.ticker, 'price': 0, 'chng': 0, 'chng%': 0}
    context = {'data': data, 'tableHeader': ['name', 'price', 'chng', 'chng%']}
    return render(request, 'layout.html', context)
