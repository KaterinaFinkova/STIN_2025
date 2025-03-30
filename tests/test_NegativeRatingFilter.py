import unittest
from models.Filters import NegativeRatingFilter
from models.StockInfo import StockInfo

class TestNegativeRatingFilter(unittest.TestCase):
    
    def test_filter_ok(self):
        stocks = [
            StockInfo("Apple", 20240329, 5, 1),
            StockInfo("Tesla", 20240329, -3, 0),
            StockInfo("Amazon", 20240329, 8, 1),
            StockInfo("XYZ Corp", 20240329, -7, 1),
        ]
        filter_instance = NegativeRatingFilter()
        filtered_stocks = filter_instance.filter(stocks)

        expected_names = {"Apple", "Amazon"}
        actual_names = {stock.name for stock in filtered_stocks}

        self.assertEqual(actual_names, expected_names)

    def test_filter_all_negative(self):
        stocks = [
            StockInfo("Tesla", 20240329, -7, 1),
            StockInfo("Ford", 20240329, -2, 1),
        ]
        filter_instance = NegativeRatingFilter()
        filtered_stocks = filter_instance.filter(stocks)

        self.assertEqual(filtered_stocks, [])

    def test_filter_no_negative(self):
        stocks = [
            StockInfo("Apple", 20240329, 5, 1),
            StockInfo("Amazon", 20240329, 8, 1),
        ]
        filter_instance = NegativeRatingFilter()
        filtered_stocks = filter_instance.filter(stocks)

        self.assertEqual(filtered_stocks, stocks)

    def test_filter_empty(self):
        stocks = []
        filter_instance = NegativeRatingFilter()
        filtered_stocks = filter_instance.filter(stocks)

        self.assertEqual(filtered_stocks, [])