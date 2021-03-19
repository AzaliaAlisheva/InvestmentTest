import json
import random
import requests

SERVICES = {
    "finnhub": "https://finnhub.io/api/v1/quote?symbol={ticker}&token=sandbox_c0t96iv48v6r4maen2gg",
}


class StockTickerScraper:
    def_service = 'finnhub'
    url = None
    def_ticker = 'AAPL'

    def __init__(self, service=def_service, ticker=def_ticker):
        self.service = service
        self.url = SERVICES[service]
        self.ticker = ticker

    def scrape_finnhub(self, url=None):
        if url is None:
            return "", 0
        r = requests.get(url).json()
        pc = r['pc']
        return pc

    def scrape(self, ticker=None):
        to_scrape_ticker = ticker or self.ticker
        if to_scrape_ticker is None:
            to_scrape_ticker = "AAPL"
        url = self.url.format(ticker=to_scrape_ticker)
        func = getattr(self, f"scrape_{self.service}")
        pc = func(url)
        return pc