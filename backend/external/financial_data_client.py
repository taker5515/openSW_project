import yfinance as yf
import pandas as pd
from typing import Optional


class FinancialDataClient:
    def get_ticker(self, symbol: str) -> yf.Ticker:
        return yf.Ticker(symbol)

    def get_income_statement(self, symbol: str, period: str = "annual") -> Optional[pd.DataFrame]:
        try:
            ticker = self.get_ticker(symbol)
            if period == "quarterly":
                return ticker.quarterly_income_stmt
            return ticker.income_stmt
        except Exception:
            return None

    def get_balance_sheet(self, symbol: str, period: str = "annual") -> Optional[pd.DataFrame]:
        try:
            ticker = self.get_ticker(symbol)
            if period == "quarterly":
                return ticker.quarterly_balance_sheet
            return ticker.balance_sheet
        except Exception:
            return None

    def get_cash_flow(self, symbol: str, period: str = "annual") -> Optional[pd.DataFrame]:
        try:
            ticker = self.get_ticker(symbol)
            if period == "quarterly":
                return ticker.quarterly_cashflow
            return ticker.cashflow
        except Exception:
            return None

    def get_info(self, symbol: str) -> dict:
        try:
            ticker = self.get_ticker(symbol)
            return ticker.info or {}
        except Exception:
            return {}


financial_data_client = FinancialDataClient()
