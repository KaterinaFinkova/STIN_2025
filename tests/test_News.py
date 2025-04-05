import json
import unittest
from models.NewsItem import NewsItem
from models.News import News

class TestNewsClass(unittest.TestCase):

    def setUp(self):
        self.company_names = {"Apple", "Tesla", "Google"}
        self.news = News(self.company_names)

    """
    def test_add_symbol_mapping(self):
        self.news.addSymbolMapping("Apple", "AAPL")
        self.news.addSymbolMapping("Tesla", "TSLA")
        self.assertEqual(self.news.symbol_to_company["Apple"], "AAPL")
        self.assertEqual(self.news.symbol_to_company["Tesla"], "TSLA")

    def test_newsCount(self):
        json_data = json.dumps([
            {"headline": "Apple News", "summary": "Apple is doing well", "related": "AAPL"}
        ])
        
        self.news.addSymbolMapping("Apple", "AAPL")
        self.news.JSONtoNewsFinnhub(json_data)
        self.assertEqual(self.news.newsCount("Apple"), 1)
        self.assertEqual(self.news.newsCount("Tesla"), 0)

    def test_missingNewsCompanies(self):
        json_data = json.dumps([
            {"headline": "Apple News", "summary": "Apple is doing well", "related": "AAPL"}
        ])
        
        self.news.addSymbolMapping("Apple", "AAPL")
        self.news.JSONtoNewsFinnhub(json_data)
        self.assertEqual(self.news.missingNewsCompanies(), {"Tesla", "Google"})

    """