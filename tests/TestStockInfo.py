import unittest
from models.StockInfo import StockInfo

class TestStockInfo(unittest.TestCase):
    
    def test_create_stock_info(self):
        item = StockItem("Microsoft", 12345678, 10, 1)
        self.assertEqual(item.name, "Microsoft")
        self.assertEqual(item.date, 12345678)
        self.assertEqual(item.rating, 10)
        self.assertEqual(item.sale, 1)

    def test_stock_info_to_dict(self):
        item = StockItem("Tesla", 12345678, -5, 0)
        item_dict = item.to_dict()
        
        self.assertEqual(item_dict['name'], "Tesla")
        self.assertEqual(item_dict['date'], 12345678)
        self.assertEqual(item_dict['rating'], -5)
        self.assertEqual(item_dict['sale'], 0)