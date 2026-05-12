import json
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: registers all models with Base.metadata

_THEMES = [
    {
        "key": "ai",
        "name": "AI & 빅테크",
        "description": "인공지능과 대형 기술주 관련 뉴스",
        "tickers": ["NVDA", "MSFT", "GOOGL", "META", "AMZN"],
    },
    {
        "key": "semiconductor",
        "name": "반도체",
        "description": "글로벌 반도체 기업 관련 뉴스",
        "tickers": ["NVDA", "AMD", "INTC", "TSM", "QCOM", "AVGO"],
    },
    {
        "key": "ev",
        "name": "전기차",
        "description": "전기차 및 배터리 관련 뉴스",
        "tickers": ["TSLA", "RIVN", "NIO", "LCID", "F", "GM"],
    },
    {
        "key": "bio",
        "name": "바이오/헬스케어",
        "description": "제약·바이오테크 관련 뉴스",
        "tickers": ["MRNA", "BNTX", "ABBV", "PFE", "JNJ", "LLY"],
    },
    {
        "key": "finance",
        "name": "금융",
        "description": "은행·증권·핀테크 관련 뉴스",
        "tickers": ["JPM", "BAC", "GS", "V", "MA", "PYPL"],
    },
]


def _seed_themes(db: Session) -> None:
    from app.models.theme import Theme

    if db.query(Theme).count() > 0:
        return
    for t in _THEMES:
        db.add(Theme(
            key=t["key"],
            name=t["name"],
            description=t["description"],
            tickers=json.dumps(t["tickers"]),
        ))
    db.commit()


def _seed_demo_user(db: Session) -> None:
    from app.models.user import User
    from app.core.security import hash_password

    if db.query(User).count() > 0:
        return
    db.add(User(
        id=1,
        email="demo@example.com",
        hashed_password=hash_password("demo1234"),
    ))
    db.commit()


def init_db() -> None:
    from app.db.session import SessionLocal

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _seed_themes(db)
        _seed_demo_user(db)
    finally:
        db.close()
