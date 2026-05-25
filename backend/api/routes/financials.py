from fastapi import APIRouter, HTTPException, Query

from external.financial_data_client import financial_data_client
from services import financial_statement_service, financial_ratio_service
from services import financial_analysis_service, financial_segment_service

router = APIRouter(prefix="/financials", tags=["financials"])


def _build_chart_data(income_data, balance_data, cashflow_data, ratios_data) -> dict:
    return {
        "revenue": [{"period": d["period"], "value": d.get("revenue")} for d in income_data],
        "net_income": [{"period": d["period"], "value": d.get("net_income")} for d in income_data],
        "free_cash_flow": [{"period": d["period"], "value": d.get("free_cash_flow")} for d in cashflow_data],
        "operating_income": [{"period": d["period"], "value": d.get("operating_income")} for d in income_data],
        "margins": [
            {
                "period": r["period"],
                "gross_margin": r.get("gross_margin"),
                "operating_margin": r.get("operating_margin"),
                "net_margin": r.get("net_margin"),
            }
            for r in ratios_data
        ],
        "debt_ratio": [{"period": r["period"], "value": r.get("debt_ratio")} for r in ratios_data],
    }


@router.get("/{symbol}/income-statement")
def get_income_statement(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        df = financial_data_client.get_income_statement(symbol, period)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")
        income_data = financial_statement_service.normalize_income_statement(df, symbol, period)
        if not income_data:
            raise HTTPException(status_code=404, detail=f"No income statement data found for {symbol}")

        info = financial_data_client.get_info(symbol)
        currency = info.get("financialCurrency") or info.get("currency")

        chart_data = {
            "revenue": [{"period": d["period"], "value": d.get("revenue")} for d in income_data],
            "gross_profit": [{"period": d["period"], "value": d.get("gross_profit")} for d in income_data],
            "operating_income": [{"period": d["period"], "value": d.get("operating_income")} for d in income_data],
            "net_income": [{"period": d["period"], "value": d.get("net_income")} for d in income_data],
        }

        return {"symbol": symbol, "period": period, "currency": currency,
                "data": income_data, "chart_data": chart_data, "message": None}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve income statement for {symbol}")


@router.get("/{symbol}/balance-sheet")
def get_balance_sheet(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        df = financial_data_client.get_balance_sheet(symbol, period)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")
        balance_data = financial_statement_service.normalize_balance_sheet(df, symbol, period)
        if not balance_data:
            raise HTTPException(status_code=404, detail=f"No balance sheet data found for {symbol}")

        info = financial_data_client.get_info(symbol)
        currency = info.get("financialCurrency") or info.get("currency")

        chart_data = {
            "total_assets": [{"period": d["period"], "value": d.get("total_assets")} for d in balance_data],
            "total_liabilities": [{"period": d["period"], "value": d.get("total_liabilities")} for d in balance_data],
            "total_equity": [{"period": d["period"], "value": d.get("total_equity")} for d in balance_data],
            "cash_and_cash_equivalents": [{"period": d["period"], "value": d.get("cash_and_cash_equivalents")} for d in balance_data],
        }

        return {"symbol": symbol, "period": period, "currency": currency,
                "data": balance_data, "chart_data": chart_data, "message": None}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve balance sheet for {symbol}")


@router.get("/{symbol}/cash-flow")
def get_cash_flow(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        df = financial_data_client.get_cash_flow(symbol, period)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")
        cashflow_data = financial_statement_service.normalize_cash_flow(df, symbol, period)
        if not cashflow_data:
            raise HTTPException(status_code=404, detail=f"No cash flow data found for {symbol}")

        info = financial_data_client.get_info(symbol)
        currency = info.get("financialCurrency") or info.get("currency")

        chart_data = {
            "operating_cash_flow": [{"period": d["period"], "value": d.get("operating_cash_flow")} for d in cashflow_data],
            "investing_cash_flow": [{"period": d["period"], "value": d.get("investing_cash_flow")} for d in cashflow_data],
            "financing_cash_flow": [{"period": d["period"], "value": d.get("financing_cash_flow")} for d in cashflow_data],
            "free_cash_flow": [{"period": d["period"], "value": d.get("free_cash_flow")} for d in cashflow_data],
        }

        return {"symbol": symbol, "period": period, "currency": currency,
                "data": cashflow_data, "chart_data": chart_data, "message": None}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve cash flow for {symbol}")


@router.get("/{symbol}/ratios")
def get_ratios(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        income_df = financial_data_client.get_income_statement(symbol, period)
        balance_df = financial_data_client.get_balance_sheet(symbol, period)
        cashflow_df = financial_data_client.get_cash_flow(symbol, period)

        income_data = financial_statement_service.normalize_income_statement(income_df, symbol, period)
        balance_data = financial_statement_service.normalize_balance_sheet(balance_df, symbol, period)
        cashflow_data = financial_statement_service.normalize_cash_flow(cashflow_df, symbol, period)

        if not income_data:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")

        ratios_data = financial_ratio_service.calculate_ratios(income_data, balance_data, cashflow_data, period)

        info = financial_data_client.get_info(symbol)
        currency = info.get("financialCurrency") or info.get("currency")

        chart_data = {
            "gross_margin": [{"period": r["period"], "value": r.get("gross_margin")} for r in ratios_data],
            "operating_margin": [{"period": r["period"], "value": r.get("operating_margin")} for r in ratios_data],
            "net_margin": [{"period": r["period"], "value": r.get("net_margin")} for r in ratios_data],
            "roe": [{"period": r["period"], "value": r.get("roe")} for r in ratios_data],
            "current_ratio": [{"period": r["period"], "value": r.get("current_ratio")} for r in ratios_data],
        }

        return {"symbol": symbol, "period": period, "currency": currency,
                "data": ratios_data, "chart_data": chart_data, "message": None}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve ratios for {symbol}")


@router.get("/{symbol}/segments")
def get_segments(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        return financial_segment_service.get_segments(symbol, period)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve segment data for {symbol}")


@router.get("/{symbol}/summary")
def get_summary(
    symbol: str,
    period: str = Query("annual", enum=["annual", "quarterly"]),
):
    symbol = symbol.upper()
    try:
        income_df = financial_data_client.get_income_statement(symbol, period)
        balance_df = financial_data_client.get_balance_sheet(symbol, period)
        cashflow_df = financial_data_client.get_cash_flow(symbol, period)

        income_data = financial_statement_service.normalize_income_statement(income_df, symbol, period)
        balance_data = financial_statement_service.normalize_balance_sheet(balance_df, symbol, period)
        cashflow_data = financial_statement_service.normalize_cash_flow(cashflow_df, symbol, period)

        if not income_data:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")

        ratios_data = financial_ratio_service.calculate_ratios(income_data, balance_data, cashflow_data, period)
        analysis = financial_analysis_service.analyze(ratios_data)
        segments = financial_segment_service.get_segments(symbol, period)

        info = financial_data_client.get_info(symbol)
        currency = info.get("financialCurrency") or info.get("currency")
        company_name = info.get("longName") or info.get("shortName") or symbol

        chart_data = _build_chart_data(income_data, balance_data, cashflow_data, ratios_data)

        return {
            "symbol": symbol,
            "period": period,
            "company_name": company_name,
            "currency": currency,
            "income_statement": income_data,
            "balance_sheet": balance_data,
            "cash_flow": cashflow_data,
            "ratios": ratios_data,
            "segments": segments,
            "analysis": analysis,
            "chart_data": chart_data,
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Failed to retrieve summary for {symbol}")
