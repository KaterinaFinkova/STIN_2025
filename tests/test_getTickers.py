import unittest
from models.getTickers import getTickers

class TestGetTickers(unittest.TestCase):

    def test_exact_match_case_insensitive(self):
        data = [
            {"name": "Apple Inc.", "symbol": "AAPL", "exchangeShortName": "NASDAQ"},
            {"name": "apple inc.", "symbol": "AAPL", "exchangeShortName": "NASDAQ"},
        ]
        result = getTickers("APPLE INC.", data)
        self.assertEqual(len(result), 2)

    def test_nasdaq_match(self):
        data = [
            {"name": "Microsoft Corporation", "symbol": "MSFT", "exchangeShortName": "NASDAQ"},
            {"name": "The Microsoft Corporation", "symbol": "MSF", "exchangeShortName": "NYSE"},
        ]
        result = getTickers("Microsoft", data)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(d["exchangeShortName"] in ["NASDAQ", "NYSE"] for d in result))

    def test_special_match(self):
        data = [
            {"name": "Tesla Motors", "symbol": "TSLA.Q", "exchangeShortName": "OTC"},
            {"name": "Tesla Motors", "symbol": "TSLA-B", "exchangeShortName": "OTC"},
        ]
        result = getTickers("Tesla", data)
        self.assertEqual(len(result), 2)
        self.assertTrue(all("." in d["symbol"] or "-" in d["symbol"] for d in result))

    def test_other_match(self):
        data = [
            {"name": "Alphabet Holdings", "symbol": "GOOG", "exchangeShortName": "LSE"},
        ]
        result = getTickers("Alphabet", data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["exchangeShortName"], "LSE")

    def test_missing_fields(self):
        data = [
            {"symbol": "MSFT", "exchangeShortName": "NASDAQ"},
            {"name": "Google LLC", "symbol": "GOOG"},
            {"symbol": "GOOG"},
        ]
        result = getTickers("Google", data)
        self.assertEqual(len(result), 1)

    def test_no_matches(self):
        data = [
            {"name": "Amazon", "symbol": "AMZN", "exchangeShortName": "NASDAQ"},
        ]
        result = getTickers("Netflix", data)
        self.assertEqual(result, [])

    def test_priority_order(self):
        data = [
            {"name": "Netflix", "symbol": "NFLX", "exchangeShortName": "NASDAQ"},
            {"name": "Netflix Streaming", "symbol": "NFLX-Q", "exchangeShortName": "OTC"},
        ]
        result = getTickers("Netflix", data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Netflix")