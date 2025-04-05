import json

class StockInfo:
    def __init__(self, name, date, rating, sale):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid name: must be a non-empty string")
        
        if not isinstance(date, int) or date <= 0:
            raise ValueError("Invalid date: must be a positive integer")
        
        if not isinstance(rating, int) or rating < -10 or rating > 10:
            raise ValueError("Invalid rating: must be between -10 and 10")
        
        if sale not in [0, 1]:
            raise ValueError("Invalid sale: must be 0 (no) or 1 (yes)")
        
        self.name = name
        self.date = date        # timestamp format !
        self.rating = rating
        self.sale = sale

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "rating": self.rating,
            "sale": self.sale
        }

    def get_sell(self):
        return self.sale

    def get_name(self):
        return self.name

    @staticmethod
    def from_dict(data):
        return StockInfo(
            name=data['name'],
            date=data['date'],
            rating=data['rating'],
            sale=data['sale']
        )

    @staticmethod
    def JSONtoList(JSON):
        """
        Converts a JSON string into a list of valid StockInfo objects
        Skips invalid entries
        Raises errors - JSON is not list of stock items, invalid JSON format
        """
        try:
            data_list = json.loads(JSON)
            if not isinstance(data_list, list):
                raise ValueError("JSON must be a list of stock items")

            stock_items = []
            for data in data_list:
                try:
                    stock_items.append(StockInfo.from_dict(data))
                except ValueError:
                    pass
            
            return stock_items

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    @staticmethod
    def ListToJSON(stock_list):
        """
        Converts a list of StockInfo objects to a JSON string
        """
        return json.dumps([item.to_dict() for item in stock_list])