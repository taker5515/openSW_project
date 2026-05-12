from sqlalchemy.orm import Session
from app.models.theme import Theme


def get_all(db: Session) -> list[Theme]:
    return db.query(Theme).all()


def get_by_key(db: Session, key: str) -> Theme | None:
    return db.query(Theme).filter(Theme.key == key).first()
