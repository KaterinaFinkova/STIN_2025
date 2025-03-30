import json

KEY_MIN_NEWS = "min_news"
KEY_MIN_SCORE = "min_score"

class UserDataManager:


    def __init__(self):
        with open("./Data/User_data.json","r",encoding="utf-8") as f:
            self.data = json.load(f)


    def get_value(self,key):
        if self.data.contains(key):
            return self.data[key];
        return None

    def set_value(self,key,value):
        if type(self.data[key])==type(value):
            print(value)
            self.data[key] = value

    def save_values(self):
        with open("./Data/User_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
