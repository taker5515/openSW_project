
def test_stock_summary_mock(client):
    r = client.get("/api/v1/stocks/AAPL/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["ticker"] == "AAPL"
    assert "price" in data
    assert isinstance(data["history"], list)


def test_stock_chart_mock(client):
    r = client.get("/api/v1/stocks/NVDA/chart?period=3mo&interval=1d")
    assert r.status_code == 200
    data = r.json()
    assert data["ticker"] == "NVDA"
    assert isinstance(data["points"], list)
    assert len(data["points"]) > 0


def test_themes_list(client):
    r = client.get("/api/v1/themes")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert data["total"] >= 1


def test_news_latest(client):
    r = client.get("/api/v1/news/latest")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data


def test_watchlist_get(client):
    r = client.get("/api/v1/watchlist")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
