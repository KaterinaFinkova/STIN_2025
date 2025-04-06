class NewsItem:
    def __init__(self, headline, text):
        self.headline = headline
        self.text = text

    def getText(self):
        return f"{self.headline}" # {self.text}"