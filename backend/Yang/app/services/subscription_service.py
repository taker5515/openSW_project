from sqlalchemy.orm import Session
from app.repositories import subscription_repository
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut, SubscriptionUpdate


def create(db: Session, data: SubscriptionCreate, user_id: int | None = None) -> SubscriptionOut:
    sub = subscription_repository.create(db, data, user_id)
    return SubscriptionOut.model_validate(sub)


def get_by_email(db: Session, email: str) -> list[SubscriptionOut]:
    subs = subscription_repository.get_by_email(db, email)
    return [SubscriptionOut.model_validate(s) for s in subs]


def update(db: Session, sub_id: int, data: SubscriptionUpdate) -> SubscriptionOut | None:
    updated = subscription_repository.update(db, sub_id, data.model_dump(exclude_none=True))
    if not updated:
        return None
    return SubscriptionOut.model_validate(updated)


def delete(db: Session, sub_id: int) -> bool:
    return subscription_repository.delete(db, sub_id)


def unsubscribe(db: Session, email: str) -> int:
    return subscription_repository.deactivate_by_email(db, email)
