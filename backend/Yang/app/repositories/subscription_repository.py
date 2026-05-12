import json
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate


def create(db: Session, data: SubscriptionCreate, user_id: int | None = None) -> Subscription:
    sub = Subscription(
        email=data.email,
        user_id=user_id,
        themes=json.dumps(data.themes),
        tickers=json.dumps(data.tickers),
        frequency=data.frequency,
        send_time=data.send_time,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def get_by_email(db: Session, email: str) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.email == email).all()


def get_by_id(db: Session, sub_id: int) -> Subscription | None:
    return db.query(Subscription).filter(Subscription.id == sub_id).first()


def update(db: Session, sub_id: int, data: dict) -> Subscription | None:
    sub = get_by_id(db, sub_id)
    if not sub:
        return None
    for key, val in data.items():
        if val is None:
            continue
        if key in ("themes", "tickers"):
            setattr(sub, key, json.dumps(val))
        else:
            setattr(sub, key, val)
    db.commit()
    db.refresh(sub)
    return sub


def delete(db: Session, sub_id: int) -> bool:
    sub = get_by_id(db, sub_id)
    if not sub:
        return False
    db.delete(sub)
    db.commit()
    return True


def deactivate_by_email(db: Session, email: str) -> int:
    subs = get_by_email(db, email)
    count = 0
    for sub in subs:
        sub.is_active = False
        count += 1
    db.commit()
    return count
