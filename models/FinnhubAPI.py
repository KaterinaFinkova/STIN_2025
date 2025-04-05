import finnhub
from typing import List
from .APIClient import APIClient

class FinnhubAPI(APIClient):
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)

    def get_news(self, tickers: List[str], from_date: str, to_date: str) -> str:
        news_data = []
        for ticker in tickers:
            try:
                company_news = self.client.company_news(ticker, _from=from_date, to=to_date)
                news_data.extend(company_news)
            except Exception as e:
                pass
        return json.dumps(news_data)