"""Stock list service - provides the master list of supported tickers by sector."""

STOCK_LIST = {
    "tech": [
        "NVDA", "MSFT", "GOOGL", "META", "AMZN", "AAPL", "AVGO", "AMD", "MU", "QCOM",
        "TSM", "ASML", "AMAT", "LRCX", "ORCL", "CRM", "NOW", "ADBE", "NFLX", "DIS",
    ],
    "consumer": [
        "WMT", "COST", "AMZN", "HD", "LOW", "MCD", "CMG", "SBUX", "KO", "PEP",
        "PG", "CL", "NKE", "LULU", "ABNB", "BKNG", "UBER", "DASH", "V", "MA",
    ],
    "industrial": ["ETN", "VRT", "GEV", "PWR", "CAT", "NEE", "EQIX", "PLD", "XOM", "RTX"],
    "finance": [
        "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "BX", "KKR", "APO",
        "BRK-B", "AXP", "COF", "V", "MA", "PYPL", "COIN", "CME", "ICE", "SPGI",
    ],
    "healthcare": ["LLY", "NVO", "JNJ", "MRK", "PFE", "ABBV", "AMGN", "ISRG", "BSX"],
}

ALL_TICKERS: list[str] = list(set(t for tickers in STOCK_LIST.values() for t in tickers))

COMPANY_NAMES: dict[str, str] = {
    "NVDA": "NVIDIA", "MSFT": "Microsoft", "GOOGL": "Alphabet", "META": "Meta Platforms",
    "AMZN": "Amazon", "AAPL": "Apple", "AVGO": "Broadcom", "AMD": "AMD", "MU": "Micron",
    "QCOM": "Qualcomm", "TSM": "TSMC", "ASML": "ASML", "AMAT": "Applied Materials",
    "LRCX": "Lam Research", "ORCL": "Oracle", "CRM": "Salesforce", "NOW": "ServiceNow",
    "ADBE": "Adobe", "NFLX": "Netflix", "DIS": "Disney", "WMT": "Walmart",
    "COST": "Costco", "HD": "Home Depot", "LOW": "Lowe's", "MCD": "McDonald's",
    "CMG": "Chipotle", "SBUX": "Starbucks", "KO": "Coca-Cola", "PEP": "PepsiCo",
    "PG": "Procter & Gamble", "CL": "Colgate", "NKE": "Nike", "LULU": "Lululemon",
    "ABNB": "Airbnb", "BKNG": "Booking Holdings", "UBER": "Uber", "DASH": "DoorDash",
    "V": "Visa", "MA": "Mastercard", "ETN": "Eaton", "VRT": "Vertiv",
    "GEV": "GE Vernova", "PWR": "Quanta Services", "CAT": "Caterpillar",
    "NEE": "NextEra Energy", "EQIX": "Equinix", "PLD": "Prologis",
    "XOM": "Exxon Mobil", "RTX": "RTX", "JPM": "JPMorgan Chase",
    "BAC": "Bank of America", "WFC": "Wells Fargo", "C": "Citigroup",
    "GS": "Goldman Sachs", "MS": "Morgan Stanley", "BLK": "BlackRock",
    "BX": "Blackstone", "KKR": "KKR", "APO": "Apollo Global",
    "BRK-B": "Berkshire Hathaway", "AXP": "American Express", "COF": "Capital One",
    "PYPL": "PayPal", "COIN": "Coinbase", "CME": "CME Group",
    "ICE": "Intercontinental Exchange", "SPGI": "S&P Global",
    "LLY": "Eli Lilly", "NVO": "Novo Nordisk", "JNJ": "Johnson & Johnson",
    "MRK": "Merck", "PFE": "Pfizer", "ABBV": "AbbVie", "AMGN": "Amgen",
    "ISRG": "Intuitive Surgical", "BSX": "Boston Scientific",
}


def get_stock_list() -> dict:
    return STOCK_LIST


def is_valid_ticker(ticker: str) -> bool:
    return ticker.upper() in ALL_TICKERS


def get_company_name(ticker: str) -> str:
    return COMPANY_NAMES.get(ticker.upper(), ticker.upper())
