STOCK_LIST = {
    "tech": ["NVDA", "MSFT", "GOOGL", "META", "AMZN", "AAPL", "AVGO", "AMD", "MU", "QCOM", "TSM", "ASML", "AMAT", "LRCX", "ORCL", "CRM", "NOW", "ADBE", "NFLX", "DIS"],
    "consumer": ["WMT", "COST", "AMZN", "HD", "LOW", "MCD", "CMG", "SBUX", "KO", "PEP", "PG", "CL", "NKE", "LULU", "ABNB", "BKNG", "UBER", "DASH", "V", "MA"],
    "industrial": ["ETN", "VRT", "GEV", "PWR", "CAT", "NEE", "EQIX", "PLD", "XOM", "RTX"],
    "finance": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "BX", "KKR", "APO", "BRK-B", "AXP", "COF", "V", "MA", "PYPL", "COIN", "CME", "ICE", "SPGI"],
    "healthcare": ["LLY", "NVO", "JNJ", "MRK", "PFE", "ABBV", "AMGN", "ISRG", "BSX"]
}

ALL_TICKERS = list(set([ticker for tickers in STOCK_LIST.values() for ticker in tickers]))
