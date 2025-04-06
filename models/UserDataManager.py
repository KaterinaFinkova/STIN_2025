import json
import os

#krok 1 odfiltrovat:
KEY_MIN_NEWS = "min_news"# Mají málo zpráv k dispozici (UI pro všechny spolecne)
KEY_MIN_SCORE = "min_score"# Která mají negativní hodnocení

#kro 2 koupit
KEY_BUY = "buy"# set buy to this

PATH_USER_DATA = "./data/User_data.json"
DEFAULT_DATA = {KEY_MIN_NEWS:1,KEY_MIN_SCORE:-10,KEY_BUY:1}
class UserDataManager:
    def __init__(self):
        if not os.path.exists(PATH_USER_DATA):
            with open(PATH_USER_DATA, 'w') as f:
                json.dump(DEFAULT_DATA, f, indent=4)
        with open(PATH_USER_DATA,"r",encoding="utf-8") as f:
            self.data = json.load(f)


    def get_value(self,key):
        if key in self.data:
            return self.data[key]
        return None

    def set_value(self,key,value):
        self.data[key] = value

    def save_values(self):
        with open(PATH_USER_DATA, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def get_data(self):
        return self.data
