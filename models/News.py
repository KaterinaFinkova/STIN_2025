import json
from collections import defaultdict
from typing import Set, List, Dict
from .NewsItem import NewsItem

class News:
    def __init__(self, company_names: set):
        self.news_data = {company: [] for company in company_names}
        self.symbol_to_company = {}
        self.company_to_symbol = defaultdict(set)

    def addSymbolMapping(self, company_name: str, symbols: list):
        for symbol in symbols:
            if symbol not in self.symbol_to_company:
                self.symbol_to_company[symbol] = company_name
                self.company_to_symbol[company_name].add(symbol)

    def getArticles(self, company: str):
        return self.news_data.get(company, [])

    def FinnhubtoNews(self, company_news: list):
        for item in company_news:
            symbol = item.get('related', "").strip()
            if not symbol:
                continue

            try:
                company = self.symbol_to_company[symbol]
            except KeyError:
                continue

            news_item = NewsItem(item['headline'], item['summary'])

            self.news_data[company].append(news_item)

    def newsCount(self, company: str) -> int:
        return len(self.news_data.get(company, []))