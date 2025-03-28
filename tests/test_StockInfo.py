import unittest
import json
from models.StockInfo import StockInfo

class TestStockInfo(unittest.TestCase):
    
    def test_create_stock_info(self):
        item = StockInfo("Microsoft", 12345678, 10, 1)
        self.assertEqual(item.name, "Microsoft")
        self.assertEqual(item.date, 12345678)
        self.assertEqual(item.rating, 10)
        self.assertEqual(item.sale, 1)

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            StockInfo("", 20240326, 5, 0)
        with self.assertRaises(ValueError):
            StockInfo(123, 20240326, 5, 0)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            StockInfo("Tesla", -20240326, 7, 1)
        with self.assertRaises(ValueError):
            StockInfo("Tesla", "20240326", 7, 1)

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            StockInfo("Apple", 20240326, 20, 0)
        with self.assertRaises(ValueError):
            StockInfo("Apple", 20240326, -15, 0)
        with self.assertRaises(ValueError):
            StockInfo("Apple", 20240326, "high", 0)

    def test_invalid_sale(self):
        with self.assertRaises(ValueError):
            StockInfo("Google", 20240326, 6, 2)
        with self.assertRaises(ValueError):
            StockInfo("Google", 20240326, 6, -1)
        with self.assertRaises(ValueError):
            StockInfo("Google", 20240326, 6, "yes")

    def test_stock_info_to_dict(self):
        item = StockInfo("Tesla", 12345678, -5, 0)
        item_dict = item.to_dict()
        
        self.assertEqual(item_dict['name'], "Tesla")
        self.assertEqual(item_dict['date'], 12345678)
        self.assertEqual(item_dict['rating'], -5)
        self.assertEqual(item_dict['sale'], 0)

    def test_from_dict(self):
        data = {
            "name": "Netflix",
            "date": 20240326,
            "rating": 5,
            "sale": 1
        }
        item = StockInfo.from_dict(data)
        self.assertEqual(item.name, "Netflix")
        self.assertEqual(item.date, 20240326)
        self.assertEqual(item.rating, 5)
        self.assertEqual(item.sale, 1)

    def test_json_to_list(self):
        json_data = '''
        [
            {"name": "Microsoft", "date": 20240326, "rating": 8, "sale": 1},
            {"name": "", "date": 20240326, "rating": 5, "sale": 0},  
            {"name": "Tesla", "date": -123456, "rating": 3, "sale": 1},  
            {"name": "Apple", "date": 20240326, "rating": 20, "sale": 0},  
            {"name": "Google", "date": 20240326, "rating": -5, "sale": 0}
        ]
        '''
        stock_list = StockInfo.JSONtoList(json_data)
        
        self.assertEqual(len(stock_list), 2)
        self.assertEqual(stock_list[0].name, "Microsoft")
        self.assertEqual(stock_list[1].name, "Google")

    def test_invalid_json_format(self):
        invalid_json = "{"
        with self.assertRaises(ValueError) as context:
            StockInfo.JSONtoList(invalid_json)
        self.assertEqual(str(context.exception), "Invalid JSON format")

    def test_json_not_list(self):
        invalid_json = '{"name": "AAPL", "date": 1672531200, "rating": 5, "sale": 1}'
        with self.assertRaises(ValueError) as context:
            StockInfo.JSONtoList(invalid_json)
        self.assertEqual(str(context.exception), "JSON must be a list of stock items")

    def test_list_to_json(self):
        items = [
            StockInfo("Microsoft", 20240326, 8, 1),
            StockInfo("Google", 20240326, -5, 0)
        ]
        json_output = StockInfo.ListToJSON(items)
        expected_json = json.dumps([
            {"name": "Microsoft", "date": 20240326, "rating": 8, "sale": 1},
            {"name": "Google", "date": 20240326, "rating": -5, "sale": 0}
        ])

        self.assertEqual(json.loads(json_output), json.loads(expected_json))