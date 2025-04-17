import json
import unittest
import requests

from Application import app
from models.UserDataManager import KEY_BUY


class TestSaleStock(unittest.TestCase):
    def test_buy(self):
        with app.app_context():
            with app.test_client() as client:
                app.Portfolio.delete_all()
                data = [
                    {"name": "OpenAI", "date": 12345678, "rating": 2, "sale": 1}
                ]
                payload = json.dumps(data)
                response = client.post('/salestock', json=payload, content_type='application/json')
                data = app.Portfolio.get_data()
                to_buy = app.UserDataManager.get_value(KEY_BUY)
                self.assertEqual(to_buy,data["OpenAI"])
                self.assertEqual("200 OK",response.status)

    def test_empty_array(self):
        with app.app_context():
            with app.test_client() as client:
                app.Portfolio.delete_all()
                data = []
                payload = json.dumps(data)
                response = client.post('/salestock', json=payload,content_type='application/json')
                data = app.Portfolio.get_data()
                self.assertEqual("200 OK",response.status)
                self.assertTrue(not data)

    def test_invalid_json(self):
        with app.app_context():
            with app.test_client() as client:
                app.Portfolio.delete_all()
                data = [
                    {"name":"error", "rating":15621}
                ]
                payload = json.dumps(data)
                response = client.post('/salestock', json=payload,content_type='application/json')
                self.assertEqual("415 UNSUPPORTED MEDIA TYPE", response.status)

