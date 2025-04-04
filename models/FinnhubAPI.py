import finnhub
import time
from typing import List
from models.News import NewsItem

class FinnhubAPI:
    def __init__(self, api_key: str):
        self.client = finnhub.Client(api_key=api_key)

    def get_tickers(self, company_names: List[str], news: News) -> None:
        for company in company_names:
            if company not in news.symbol_to_company:
                try:
                    symbols = self.client.stock_symbols('US')  # US exchanges

                    if symbols: # Only first found symbol
                        ticker = symbols[0]['symbol']
                        news.addSymbolMapping(company, ticker) 

                except Exception as e:
                    pass

    def get_news(self, tickers: List[str], from_date: str, to_date: str) -> str:
        news_data = []
        for ticker in tickers:
            try:
                company_news = self.client.company_news(ticker, _from=from_date, to=to_date)
                news_data.extend(company_news)
            except Exception as e:
                pass
        return json.dumps(news_data)