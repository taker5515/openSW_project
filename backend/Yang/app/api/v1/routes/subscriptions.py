from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_user
from app.models.user import User
from app.schemas.subscription import (
    SubscriptionCreate, SubscriptionOut, SubscriptionUpdate, UnsubscribeRequest,
)
from app.services import subscription_service

router = APIRouter()


@router.post("", response_model=SubscriptionOut, status_code=201)
def create_subscription(
    body: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    user_id = current_user.id if current_user else None
    return subscription_service.create(db, body, user_id)


@router.get("/{email}", response_model=list[SubscriptionOut])
def get_subscriptions(email: str, db: Session = Depends(get_db)):
    return subscription_service.get_by_email(db, email)


@router.patch("/{sub_id}", response_model=SubscriptionOut)
def update_subscription(
    sub_id: int,
    body: SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    updated = subscription_service.update(db, sub_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="구독 정보를 찾을 수 없습니다.")
    return updated


@router.delete("/{sub_id}", status_code=204)
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    if not subscription_service.delete(db, sub_id):
        raise HTTPException(status_code=404, detail="구독 정보를 찾을 수 없습니다.")


@router.post("/unsubscribe")
def unsubscribe(body: UnsubscribeRequest, db: Session = Depends(get_db)):
    count = subscription_service.unsubscribe(db, body.email)
    return {"message": f"{count}개의 구독이 비활성화되었습니다.", "count": count}
