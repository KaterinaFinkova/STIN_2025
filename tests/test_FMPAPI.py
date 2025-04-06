import unittest
import os
from models.News import News
from models.FMPAPI import FMPAPI
from models.CompanySymbolMapper import CompanySymbolMapper

class TestFMPAPI(unittest.TestCase):
    def setUp(self):
        api_key = os.getenv("FMP_API_KEY")
        if not api_key:
            self.skipTest("FMP_API_KEY not set")

        self.api = FMPAPI(api_key)
        self.company_names = {"Apple", "Amazon", "Google", "Tesla", "GoPro", "Fitbit", "Ford", "Marathon Oil", "Uber", "Starbucks", "Netflix"}
        self.news = News(self.company_names, CompanySymbolMapper())

    def test_get_tickers_for_apple(self):
        self.api.get_tickers(self.news, self.company_names.copy())

        for company in self.company_names:
            if company in self.news.mapper.company_to_symbol:
                print(f"{company}: {self.news.mapper.company_to_symbol[company]}")