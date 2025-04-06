import unittest
from unittest.mock import patch, MagicMock
from models import FMPAPI, News, CompanySymbolMapper

class TestFMPAPI(unittest.TestCase):

    def setUp(self):
        self.api = FMPAPI(api_key="KEY")
        self.company_names = {
            "Apple", "Amazon", "Google"
        }
        self.news = News(self.company_names, CompanySymbolMapper())

    @patch("models.FMPAPI.requests.get")
    def test_get_tickers_successful_response(self, mock_get):
        mock_data = [
            {"symbol": "AAPL", "name": "Apple Inc", "exchangeShortName": "NASDAQ"},
            {"symbol": "AMZN", "name": "Amazon", "exchangeShortName": "NASDAQ"},
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response

        companies = {"Apple", "Amazon"}
        self.api.get_tickers(self.news, companies)

        self.assertIn("AAPL", self.news.getSymbols("Apple"))
        self.assertIn("AMZN", self.news.getSymbols("Amazon"))

        self.assertNotIn("Apple", companies)
        self.assertNotIn("Amazon", companies)

    @patch("models.FMPAPI.requests.get")
    def test_get_tickers_no_valid_matches(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        companies = {"Google"}
        self.api.get_tickers(self.news, companies)

        self.assertEqual(self.news.getSymbols("Google"), set())
        self.assertIn("Google", companies)

    @patch("models.FMPAPI.requests.get")
    def test_get_tickers_api_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        companies = {"Apple"}
        self.api.get_tickers(self.news, companies)

        self.assertEqual(self.news.getSymbols("Apple"), set())
        self.assertIn("Apple", companies)

    @patch("models.FMPAPI.requests.get")
    def test_get_tickers_exception_handling(self, mock_get):
        mock_get.side_effect = Exception("Request failed")

        companies = {"Apple"}
        self.api.get_tickers(self.news, companies)

        self.assertEqual(self.news.getSymbols("Apple"), set())
        self.assertIn("Apple", companies)