import unittest
from models.APIManager import APIManager
from models.FinnhubAPI import FinnhubAPI
from models.FMPAPI import FMPAPI
from models.News import News
import os

class TestAPIManager(unittest.TestCase):
    def setUp(self):
        self.finnhub_api_key = os.getenv("FINNHUB_API_KEY")
        self.fmp_api_key = os.getenv("FMP_API_KEY")

        finnhub_api = FinnhubAPI(api_key=self.finnhub_api_key)
        fmp_api = FMPAPI(api_key=self.fmp_api_key)

        self.api_manager = APIManager(
            tickers_apis=[finnhub_api, fmp_api],
            news_apis=[finnhub_api, fmp_api]
        )

    def test_fetch_news_for_company(self):
        company_names = {"Apple", "Tesla", "Amazon"}

        news = self.api_manager.fetch_news(company_names, "2025-04-01", "2025-04-02")

        self.assertIn("Apple", news.company_to_symbol)
        self.assertIn("Tesla", news.company_to_symbol)
        self.assertIn("Amazon", news.company_to_symbol)

        #for name, articles in news.news_data.items() :
            #print(name)
            #for article in articles:
                #print(article.headline)

        self.assertGreater(len(news.company_to_symbol["Apple"]), 0, "Apple should have news data")
        self.assertGreater(len(news.company_to_symbol["Tesla"]), 0, "Tesla should have news data")
        self.assertGreater(len(news.company_to_symbol["Amazon"]), 0, "Amazon should have news data")
