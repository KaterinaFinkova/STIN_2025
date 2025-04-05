import re

def getTickers(company_name, data):
    nasdaq_matches = []
    other_matches = []
    special_matches = []

    for item in data:
        exchange = item.get("exchangeShortName", "")
        ticker_name = item.get("name", "")

        if re.search(r'\b' + re.escape(company_name) + r'\b', ticker_name, re.IGNORECASE):

            if exchange == "NASDAQ" or exchange == "NYSE":
                nasdaq_matches.append(item)

            elif '.' in item["symbol"] or '-' in item["symbol"]:
                special_matches.append(item)

            else:
                other_matches.append(item)

    if nasdaq_matches:
        return nasdaq_matches
    
    if other_matches:
        return other_matches
        
    return special_matches