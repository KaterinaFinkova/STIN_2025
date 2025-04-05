import os
import unittest
from datetime import datetime, timedelta

from models.FinnhubAPI import FinnhubAPI
from models.News import News

class TestFinnhubAPI(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv("FINNHUB_API_KEY")
        if not api_key:
            self.skipTest("FINNHUB_API_KEY not set")

        self.api = FinnhubAPI(api_key=api_key)
        self.company_name = "Apple Inc"
        self.symbol = "AAPL"

        self.news = News({self.company_name})
        self.news.addSymbolMapping(self.company_name, [self.symbol])

        today = datetime.now().date()
        self.from_date = str(today - timedelta(days=1))
        self.to_date = str(today)

    def test_get_news_single_company(self):
        company_names = {self.company_name}
        self.api.get_news(self.news, company_names, self.from_date, self.to_date)

        articles = self.news.getArticles(self.company_name)
        self.assertIsInstance(articles, list)
        self.assertGreaterEqual(len(articles), 0)

        if articles:
            self.assertNotIn(self.company_name, company_names)