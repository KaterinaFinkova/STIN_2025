import re

def getTickers(company_name, data):
    exact_matches = []
    nasdaq_matches = []
    other_matches = []
    special_matches = []

    for item in data:
        exchange = item.get("exchangeShortName", "")
        ticker_name = item.get("name", "")

        if company_name.lower() == ticker_name.lower():
            exact_matches.append(item)

        elif re.search(r'\b' + re.escape(company_name) + r'\b', ticker_name, re.IGNORECASE):

            if exchange == "NASDAQ" or exchange == "NYSE":
                nasdaq_matches.append(item)

            elif '.' in item["symbol"] or '-' in item["symbol"]:
                special_matches.append(item)

            else:
                other_matches.append(item)

    if exact_matches:
        return exact_matches

    if nasdaq_matches:
        return nasdaq_matches
    
    if other_matches:
        return other_matches
        
    return special_matches