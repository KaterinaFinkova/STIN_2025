from abc import ABC, abstractmethod
from flask import current_app as app

from models.UserDataManager import KEY_MIN_NEWS


class BeforeFilter(ABC):
    @abstractmethod
    def filter(self, stock_list, news):
        pass

class MinMessagesFilter(BeforeFilter):
    def __init__(self, min_messages):
        self.min_messages = min_messages

    def filter(self, stock_list, news):
        return [stock for stock in stock_list if news.newsCount(stock.name) >= app.UserDataManager.get_data(KEY_MIN_NEWS)]


class AfterFilter(ABC):
    @abstractmethod
    def filter(self, stock_list):
        pass

class NegativeRatingFilter(AfterFilter):
    def filter(self, stock_list):
        """Filters out stocks with negative ratings."""
        return [stock for stock in stock_list if stock.rating >= 0]