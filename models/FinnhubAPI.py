import finnhub
from typing import List
from .News import News
from .APIClient import APIClient

class FinnhubAPI(APIClient):
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)

    def get_news(self, news: News, company_names: set, from_date: str, to_date: str):
        for company_name in list(company_names):
            tickers = news.getSymbols(company_name)
            
            for ticker in tickers:
                try:
                    company_news = self.client.company_news(ticker, _from=from_date, to=to_date)
                    news.FinnhubtoNews(company_news)
                    company_names.discard(company_name)
                except Exception as e:
                    pass