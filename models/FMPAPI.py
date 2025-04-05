import requests
import urllib.parse
from .APIClient import APIClient
from .News import News
from .getTickers import getTickers

class FMPAPI(APIClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3/search"

    def get_tickers(self, news: News, company_names: set):
        print(type(company_names))
        for company_name in list(company_names):
            encoded_company_name = urllib.parse.quote(company_name)
            url = f"{self.base_url}?query={encoded_company_name}&apikey={self.api_key}"
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    continue
                data = response.json()

                tickers = getTickers(company_name, data)

                if tickers:
                    news.loadTickerData(company_name, tickers)
                    company_names.discard(company_name)
            
            except Exception as e:
                pass