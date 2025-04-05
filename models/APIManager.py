from typing import List
from .News import News
from .APIClient import APIClient
    
class APIManager:
    def __init__(self, tickers_apis: List[APIClient], news_apis: List[APIClient]):
        self.tickers_apis = tickers_apis
        self.news_apis = news_apis

    def fetch_news(self, company_names: set, from_date: str, to_date: str) -> 'News':
        news = News(company_names)

        missing_companies = company_names.copy()
        for api in self.tickers_apis:
            api.get_tickers(news, missing_companies)

        missing_companies = company_names.copy()
        for api in self.news_apis:
            api.get_news(news, missing_companies, from_date, to_date)

        return news