import requests
import json

class NewsDataAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsdata.io/api/1/news"

    def get_news(self, company_names: List[str], from_date: str, to_date: str) -> str:
        company_query = ",".join(company_names)
        params = {
            "apikey": self.api_key,
            "q": company_query,
            "from_date": from_date,
            "to_date": to_date,
            "language": "en",
            "category": "business"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return json.dumps([])