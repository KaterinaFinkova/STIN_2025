class BeforeFilter():
    @abstractmethod
    def filter(self, items):
        pass

class MinMessagesFilter(BeforeFilter):
    def __init__(self, min_messages):
        self.min_messages = min_messages

    def filter(self, items):


class AfterFilter():
    @abstractmethod
    def filter(self, items):
        pass

class NegativeRatingFilter(AfterFilter):
    def filter(self, items):