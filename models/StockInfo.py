class StockInfo:
    def __init__(self, name, date, rating, sale):
        self.name = name
        self.date = date
        self.rating = rating
        self.sale = sale

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "rating": self.rating,
            "sale": self.sale
        }

    @staticmethod
    def from_dict(data):
        return StockItem(
            name=data['name'],
            date=data['date'],
            rating=data['rating'],
            sale=data['sale']
        )

    @staticmethod 
    def JSONtoList(JSON):


    @staticmethod 
    def ListToJSON(list):