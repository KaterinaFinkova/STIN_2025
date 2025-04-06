import json
import unittest
from Application import app
from models.Portfolio import PATH_PORTFOLIO


class TestPortfolio(unittest.TestCase):
    def test_buy(self):
        with app.app_context():
            app.Portfolio.buy("pytest")
            self.assertTrue("pytest" in app.Portfolio.get_data())
            app.Portfolio.sell("pytest")
            self.assertTrue("pytest" not in app.Portfolio.get_data())

    def test_save(self):
        with app.app_context():
            app.Portfolio.buy("pytest")
            app.Portfolio.save()
        with open(PATH_PORTFOLIO, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertTrue("pytest" in data)
