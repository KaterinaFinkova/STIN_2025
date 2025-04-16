from collections import defaultdict
from .NewsItem import NewsItem
from .CompanySymbolMapper import CompanySymbolMapper

class News:
    def __init__(self, company_names: set, mapper):
        self.news_data = {company: [] for company in company_names}
        self.mapper = mapper

    def addSymbolMapping(self, company_name: str, symbols: list):
        self.mapper.addMapping(company_name, symbols)

    def addArticle(self, company: str, headline: str, summary: str):
        news_item = NewsItem(headline, summary)
        self.news_data[company].append(news_item)

    def loadTickerData(self, company_name: str, ticker_data: list):
        symbols = []
        for item in ticker_data:
            symbol = item.get("symbol")
            if symbol:
                symbols.append(symbol)
        self.mapper.addMapping(company_name, symbols)

    def getSymbols(self, company_name : str) :
        return self.mapper.getSymbols(company_name)

    def getArticles(self, company: str):
        return self.news_data.get(company, [])

    def FinnhubtoNews(self, company_news: list):
        for item in company_news:
            symbol = item.get('related', "").strip()
            if not symbol:
                continue

            company = self.mapper.getCompany(symbol)
            if not company:
                continue

            news_item = NewsItem(item['headline'], item['summary'])
            self.news_data[company].append(news_item)

    def newsCount(self, company: str) -> int:
        return len(self.news_data.get(company, []))