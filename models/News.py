import json
from bidict import bidict
from typing import Set, List, Dict
from .NewsItem import NewsItem

class News:
    def __init__(self, company_names: set):
        self.news_data = {company: [] for company in company_names}
        self.symbol_to_company = bidict()

    def addSymbolMapping(self, company_name: str, symbol: str):
        self.symbol_to_company[company_name] = symbol

    def JSONtoNewsFinnhub(self, json_data: str):
        data = json.loads(json_data)

        for item in data:
            symbol = item.get('related', "").strip()
            if not symbol:
                continue

            try:
                company = self.symbol_to_company.inverse[symbol]
            except KeyError:
                continue

            news_item = NewsItem(item['headline'], item['summary'])
            self.news_data[company].append(news_item)

    def newsCount(self, company: str) -> int:
        return len(self.news_data.get(company, []))
    
    def missingNewsCompanies(self) -> Set[str]:
        return {company for company, articles in self.news_data.items() if not articles}