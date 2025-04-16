import unittest
from models import News, CompanySymbolMapper, NewsItem
from unittest.mock import MagicMock

class TestNews(unittest.TestCase):

    def test_add_article(self):
        mock_mapper = MagicMock()
        mock_mapper.getCompany.return_value = "CompanyA"
        
        news = News({"CompanyA", "CompanyB"}, mock_mapper)

        news.addArticle("CompanyA", "Positive News", "Everything is great!")
        news.addArticle("CompanyA", "Another Positive News", "Another great thing!")
        
        articles = news.getArticles("CompanyA")
        
        self.assertEqual(len(articles), 2)
        
        self.assertEqual(articles[0].headline, "Positive News")
        self.assertEqual(articles[0].text, "Everything is great!")
        self.assertEqual(articles[1].headline, "Another Positive News")
        self.assertEqual(articles[1].text, "Another great thing!")

    def test_add_symbol_mapping(self):
        mapper = CompanySymbolMapper()
        news = News({"OpenAI"}, mapper)

        news.addSymbolMapping("OpenAI", ["OAI"])
        company_news = [{
            "related": "OAI",
            "headline": "New AI Model",
            "summary": "OpenAI just released something amazing."
        }]
        news.FinnhubtoNews(company_news)

        articles = news.getArticles("OpenAI")
        self.assertEqual(len(articles), 1)
        self.assertIsInstance(articles[0], NewsItem)
        self.assertEqual(articles[0].headline, "New AI Model")

    def test_load_ticker_data(self):
        mapper = CompanySymbolMapper()
        news = News({"Tesla"}, mapper)

        ticker_data = [{"symbol": "TSLA"}, {"symbol": "TSLAQ"}]
        news.loadTickerData("Tesla", ticker_data)

        company_news = [{
            "related": "TSLA",
            "headline": "Tesla News",
            "summary": "Stock is up."
        }]
        news.FinnhubtoNews(company_news)

        articles = news.getArticles("Tesla")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].text, "Stock is up.")

    def test_news_count(self):
        mapper = CompanySymbolMapper()
        news = News({"Tesla"}, mapper)

        news.addSymbolMapping("Tesla", ["TSLA"])
        company_news = [
            {"related": "TSLA", "headline": "Boom", "summary": "Stock boomed."},
            {"related": "TSLA", "headline": "Crash", "summary": "Then it crashed."}
        ]
        news.FinnhubtoNews(company_news)

        self.assertEqual(news.newsCount("Tesla"), 2)

    def test_get_articles_returns_empty_list(self):
        mapper = CompanySymbolMapper()
        news = News({"OpenAI"}, mapper)

        articles = news.getArticles("OpenAI")
        self.assertEqual(articles, [])

        articles = news.getArticles("DeepMind")
        self.assertEqual(articles, [])

    def test_unknown_symbol_does_not_add_news(self):
        mapper = CompanySymbolMapper()
        news = News({"OpenAI"}, mapper)

        company_news = [{
            "related": "UNKNOWN",
            "headline": "Mystery News",
            "summary": "Should not be added."
        }]
        news.FinnhubtoNews(company_news)

        self.assertEqual(news.newsCount("OpenAI"), 0)