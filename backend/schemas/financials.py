from pydantic import BaseModel
from typing import Optional, List


class IncomeStatementPeriod(BaseModel):
    period: str
    fiscal_date: Optional[str] = None
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    selling_general_admin_expense: Optional[float] = None
    research_and_development: Optional[float] = None
    operating_expense: Optional[float] = None
    operating_income: Optional[float] = None
    interest_expense: Optional[float] = None
    pretax_income: Optional[float] = None
    tax_provision: Optional[float] = None
    net_income: Optional[float] = None
    basic_eps: Optional[float] = None
    diluted_eps: Optional[float] = None
    ebitda: Optional[float] = None
    revenue_growth: Optional[float] = None
    operating_income_growth: Optional[float] = None
    net_income_growth: Optional[float] = None


class BalanceSheetPeriod(BaseModel):
    period: str
    fiscal_date: Optional[str] = None
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    cash_and_cash_equivalents: Optional[float] = None
    accounts_receivable: Optional[float] = None
    inventory: Optional[float] = None
    non_current_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    long_term_debt: Optional[float] = None
    total_equity: Optional[float] = None
    retained_earnings: Optional[float] = None


class CashFlowPeriod(BaseModel):
    period: str
    fiscal_date: Optional[str] = None
    operating_cash_flow: Optional[float] = None
    investing_cash_flow: Optional[float] = None
    financing_cash_flow: Optional[float] = None
    depreciation_and_amortization: Optional[float] = None
    change_in_working_capital: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None


class RatiosPeriod(BaseModel):
    period: str
    fiscal_date: Optional[str] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    revenue_growth: Optional[float] = None
    operating_income_growth: Optional[float] = None
    net_income_growth: Optional[float] = None
    revenue_cagr_3y: Optional[float] = None
    debt_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None
    free_cash_flow_margin: Optional[float] = None
    operating_cash_flow_to_net_income: Optional[float] = None


class AnalysisItem(BaseModel):
    category: str
    level: str
    message: str
    message_ko: str


class ChartDataPoint(BaseModel):
    period: str
    value: Optional[float] = None


class MarginDataPoint(BaseModel):
    period: str
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None


class FinancialsChartData(BaseModel):
    revenue: List[ChartDataPoint]
    net_income: List[ChartDataPoint]
    free_cash_flow: List[ChartDataPoint]
    operating_income: List[ChartDataPoint]
    margins: List[MarginDataPoint]
    debt_ratio: List[ChartDataPoint]


class IncomeStatementResponse(BaseModel):
    symbol: str
    period: str
    currency: Optional[str] = None
    data: List[IncomeStatementPeriod]
    chart_data: dict
    message: Optional[str] = None


class BalanceSheetResponse(BaseModel):
    symbol: str
    period: str
    currency: Optional[str] = None
    data: List[BalanceSheetPeriod]
    chart_data: dict
    message: Optional[str] = None


class CashFlowResponse(BaseModel):
    symbol: str
    period: str
    currency: Optional[str] = None
    data: List[CashFlowPeriod]
    chart_data: dict
    message: Optional[str] = None


class RatiosResponse(BaseModel):
    symbol: str
    period: str
    currency: Optional[str] = None
    data: List[RatiosPeriod]
    chart_data: dict
    message: Optional[str] = None


class SegmentsResponse(BaseModel):
    symbol: str
    period: str
    available: bool
    message: str
    segments: list
    chart_data: list


class SummaryResponse(BaseModel):
    symbol: str
    period: str
    company_name: Optional[str] = None
    currency: Optional[str] = None
    income_statement: List[IncomeStatementPeriod]
    balance_sheet: List[BalanceSheetPeriod]
    cash_flow: List[CashFlowPeriod]
    ratios: List[RatiosPeriod]
    segments: SegmentsResponse
    analysis: List[AnalysisItem]
    chart_data: FinancialsChartData
