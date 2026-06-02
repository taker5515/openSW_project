from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from db.session import get_db
from core.security import decode_token
from repositories.user_repository import UserRepository
from models.user import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")
    user = UserRepository(db).get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="사용자를 찾을 수 없습니다.")
    return user
