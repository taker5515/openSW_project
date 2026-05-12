import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.analysis import AnalysisResult


def get_cached(db: Session, ticker: str, analysis_type: str) -> AnalysisResult | None:
    now = datetime.now(timezone.utc)
    result = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.ticker == ticker,
            AnalysisResult.analysis_type == analysis_type,
        )
        .order_by(AnalysisResult.created_at.desc())
        .first()
    )
    if result is None:
        return None
    expires = result.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return result if expires > now else None


def save(
    db: Session,
    ticker: str,
    analysis_type: str,
    payload: dict,
    ttl_hours: int = 4,
) -> AnalysisResult:
    expires = datetime.now(timezone.utc) + timedelta(hours=ttl_hours)
    entry = AnalysisResult(
        ticker=ticker,
        analysis_type=analysis_type,
        payload=json.dumps(payload),
        expires_at=expires,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def invalidate(db: Session, ticker: str) -> None:
    db.query(AnalysisResult).filter(AnalysisResult.ticker == ticker).delete()
    db.commit()
