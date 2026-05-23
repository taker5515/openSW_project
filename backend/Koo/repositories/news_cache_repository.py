from sqlalchemy.orm import Session
from models.news_cache import NewsCache
from datetime import datetime, timezone, timedelta
import json

class NewsCacheRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, news_url: str, expire_hours: int = 1) -> dict | None:
        cache = self.db.query(NewsCache).filter(NewsCache.news_url == news_url).first()
        if not cache:
            return None
        expire_time = cache.created_at.replace(tzinfo=timezone.utc) + timedelta(hours=expire_hours)
        if datetime.now(timezone.utc) > expire_time:
            self.db.delete(cache)
            self.db.commit()
            return None
        return json.loads(cache.result)

    def set(self, ticker: str, news_url: str, result: dict):
        existing = self.db.query(NewsCache).filter(NewsCache.news_url == news_url).first()
        if existing:
            existing.result = json.dumps(result)
            existing.created_at = datetime.now(timezone.utc)
        else:
            cache = NewsCache(ticker=ticker, news_url=news_url, result=json.dumps(result))
            self.db.add(cache)
        self.db.commit()