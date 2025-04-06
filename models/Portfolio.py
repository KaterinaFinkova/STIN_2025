import json
import os

from flask import current_app as app
from models.UserDataManager import KEY_BUY

PATH_PORTFOLIO = "./data/Portfolio.json"
class Portfolio:
    def __init__(self):
        if not os.path.exists(PATH_PORTFOLIO):
            with open(PATH_PORTFOLIO, 'w') as f:   json.dump(dict(), f, indent=4)
        with open(PATH_PORTFOLIO, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def sell(self,stock):
        return self.data.pop(stock,None)

    def buy(self,stock):
        amount = app.UserDataManager.get_value(KEY_BUY)
        if stock not in self.data or amount > self.data[stock]:
            self.data[stock] = amount

    def save(self):
        with open(PATH_PORTFOLIO, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def buy_or_sell(self,stock_info):
        if stock_info.get_sell() is True:
            self.buy(stock_info.get_name())
        elif stock_info.get_sell() is False:
            self.sell(stock_info.get_name())

    def get_data(self):
        return self.data