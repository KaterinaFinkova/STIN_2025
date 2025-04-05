import json

#krok 1 odfiltrovat:
KEY_MIN_NEWS = "min_news" # Mají málo zpráv k dispozici (UI pro všechny spolecne)
KEY_MIN_SCORE = "min_score" #  Která mají negativní hodnocení

#kro 2 koupit
KEY_BUY = "buy" # set buy to this

class UserDataManager:


    def __init__(self):
        with open("./Data/User_data.json","r",encoding="utf-8") as f:
            self.data = json.load(f)


    def get_value(self,key):
        if key in self.data:
            return self.data[key]
        return None

    def set_value(self,key,value):
        print(value)
        self.data[key] = value

    def save_values(self):
        with open("./Data/User_data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
