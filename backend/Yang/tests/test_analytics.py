import pandas as pd
import pytest


def test_rsi_flat_series():
    from app.analytics.indicators import calculate_rsi
    s = pd.Series([100.0] * 20)
    rsi = calculate_rsi(s)
    assert 40 <= rsi <= 60


def test_rsi_rising_series():
    from app.analytics.indicators import calculate_rsi
    s = pd.Series([float(i) for i in range(1, 21)])
    rsi = calculate_rsi(s)
    assert rsi > 60


def test_rsi_falling_series():
    from app.analytics.indicators import calculate_rsi
    s = pd.Series([float(20 - i) for i in range(20)])
    rsi = calculate_rsi(s)
    assert rsi < 40


def test_volatility():
    from app.analytics.indicators import calculate_volatility
    s = pd.Series([100.0] * 30)
    assert calculate_volatility(s) == 0.0


def test_toss_style_mock(client):
    r = client.get("/api/v1/analytics/AAPL/toss-style")
    assert r.status_code == 200
    data = r.json()
    assert data["ticker"] == "AAPL"
    assert "sections" in data
    assert "summary_cards" in data
    assert isinstance(data["score"], float)


def test_overall_score_all_good():
    from app.analytics.scoring import calculate_overall_score
    from app.schemas.analysis import AnalysisItem, Section
    items = [AnalysisItem(key="x", label="x", value="x", status="good", description="", interpretation="")]
    sections = [Section(key="s", title="s", subtitle="s", items=items)]
    assert calculate_overall_score(sections) == 100.0


def test_overall_score_all_bad():
    from app.analytics.scoring import calculate_overall_score
    from app.schemas.analysis import AnalysisItem, Section
    items = [AnalysisItem(key="x", label="x", value="x", status="bad", description="", interpretation="")]
    sections = [Section(key="s", title="s", subtitle="s", items=items)]
    assert calculate_overall_score(sections) == 0.0
