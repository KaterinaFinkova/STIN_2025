from collections import defaultdict
from datetime import datetime, timedelta, timezone

class CompanySymbolMapper:
    def __init__(self, expiry_days=7):
        self.symbol_to_company = {}
        self.company_to_symbol = defaultdict(set)
        self.symbol_timestamp = {}
        self.expiry_duration = timedelta(days=expiry_days)

    def addMapping(self, company_name: str, symbols: list):
        now = datetime.now(timezone.utc)
        for symbol in symbols:
            if symbol not in self.symbol_to_company:
                self.symbol_to_company[symbol] = company_name
                self.company_to_symbol[company_name].add(symbol)
                self.symbol_timestamp[symbol] = now

    def getCompany(self, symbol: str) -> str:
        return self.symbol_to_company.get(symbol)
    
    def getSymbols(self, company_name : str) :
        return self.company_to_symbol.get(company_name)

    def hasSymbol(self, symbol: str) -> bool:
        return symbol in self.symbol_to_company

    def getUnknownCompanies(self, companies: set) -> set:
        self._cleanOldMappings()
        known_companies = set(self.company_to_symbol.keys())
        return companies - known_companies

    def _cleanOldMappings(self):
        now = datetime.now(timezone.utc)
        expired_symbols = [
            symbol for symbol, timestamp in self.symbol_timestamp.items()
            if now - timestamp > self.expiry_duration
        ]
        for symbol in expired_symbols:
            company = self.symbol_to_company.pop(symbol, None)
            if company:
                self.company_to_symbol[company].discard(symbol)
            self.symbol_timestamp.pop(symbol, None)