import json
import time
import News, FinnhubAPI, NewsDataAPI

class APIManager:
    def __init__(self, finnhub_api: FinnhubAPI, newsdata_api: NewsDataAPI):
        self.finnhub_api = finnhub_api
        self.newsdata_api = newsdata_api

    def fetch_news(self, company_names: set, from_date: str, to_date: str) -> 'News':
        news = News(company_names)

        self.finnhub_api.get_tickers(company_names, news)

        tickers = list(news.symbol_to_company.values())
        json_news = self._get_news_with_retry(self.finnhub_api.get_news, tickers, from_date, to_date)
        news.JSONtoNewsFinnhub(json_news)

        missing_companies = news.missingNewsCompanies()
        if missing_companies:
            json_news = self._get_news_with_retry(self.newsdata_api.get_news, list(missing_companies), from_date, to_date)
            news.JSONtoNewsNewsdata(json_news)

        return news
    
    def _get_news_with_retry(self, fetch_news_func, items, from_date: str, to_date: str) -> str:
        retries = 3
        delay = 2 
        for attempt in range(retries):
            try:
                json_news = fetch_news_func(items, from_date, to_date)
                return json_news
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                else:
                    return json.dumps([])

        return json.dumps([])