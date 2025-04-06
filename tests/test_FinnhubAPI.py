import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from models import FinnhubAPI, News, CompanySymbolMapper

class TestFinnhubAPI(unittest.TestCase):

    def test_get_news(self):
        api_key = "KEY"
        api = FinnhubAPI(api_key)
        company_name = "Apple Inc"
        symbol = "AAPL"

        news = News({company_name}, CompanySymbolMapper())
        news.addSymbolMapping(company_name, [symbol])

        from_date = str(datetime.now().date() - timedelta(days=1))
        to_date = str(datetime.now().date())

        mock_news_data = [
            {
                "related": symbol,
                "headline": "Apple releases new iPhone",
                "summary": "The iPhone 15 is here."
            },
            {
                "related": symbol,
                "headline": "Apple stock up",
                "summary": "Strong earnings report drives price."
            }
        ]

        with patch.object(api.client, 'company_news', return_value=mock_news_data) as mock_method:
            company_names = {company_name}
            api.get_news(news, company_names, from_date, to_date)

            mock_method.assert_called_once_with(symbol, _from=from_date, to=to_date)

            articles = news.getArticles(company_name)
            self.assertEqual(len(articles), 2)
            self.assertEqual(articles[0].headline, "Apple releases new iPhone")
            self.assertNotIn(company_name, company_names)

    def test_get_news_api_failure(self):
        api_key = "FAKE_KEY"
        api = FinnhubAPI(api_key)
        company_name = "Apple Inc"
        symbol = "AAPL"

        news = News({company_name}, CompanySymbolMapper())
        news.addSymbolMapping(company_name, [symbol])

        from_date = str(datetime.now().date() - timedelta(days=1))
        to_date = str(datetime.now().date())

        with patch.object(api.client, 'company_news', side_effect=Exception("API error")) as mock_method:
            company_names = {company_name}
            api.get_news(news, company_names, from_date, to_date)

            mock_method.assert_called_once()

            self.assertEqual(len(news.getArticles(company_name)), 0)
            self.assertIn(company_name, company_names)