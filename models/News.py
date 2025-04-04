import json
from typing import List, Dict
from models.NewsItem import NewsItem
from bidict import bidict

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
                company = self.symbol_to_company[symbol]
            except KeyError:
                continue

            news_item = NewsItem(item['headline'], item['summary'])
            self.news_data[company].append(news_item)

    def JSONtoNewsNewsdata(self, json_data: str):
        data = json.loads(json_data)

        for article in data.get("articles", []):
            title = article.get('title', '')
            description = article.get('description', '')

            mentioned_companies = {company for company in self.news_data if company.lower() in (title + description).lower()}

            if mentioned_companies:
                news_item = NewsItem(
                    headline=title,
                    summary=description
                )

                for company in mentioned_companies:
                    self.news_data[company].append(news_item)

    def newsCount(self, company: str) -> int:
        return len(self.news_data.get(company, []))