from django.shortcuts import render
from django.views import generic


def index(request):
    list_of_stocks = ['AAPL', 'AMZN', 'GME', 'TSLA']
    data = {}
    for stock in list_of_stocks:
        data[stock] = {'name': stock, 'price': 0, 'chng': 0, 'chng%': 0}
    context = {'list': list_of_stocks, 'data': data, 'tableHeader': ['name', 'price', 'chng', 'chng%']}
    return render(request, 'layout.html', context)
