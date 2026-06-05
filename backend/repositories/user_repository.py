from sqlalchemy.orm import Session
from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, email: str, hashed_password: str = None, name: str = None) -> User:
        user = User(email=email, hashed_password=hashed_password, name=name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_or_create_google_user(self, email: str, name: str = None) -> User:
        user = self.get_by_email(email)
        if user is None:
            user = self.create(email=email, name=name)
        elif name and not user.name:
            user.name = name
            self.db.commit()
            self.db.refresh(user)
        return user

    def update_themes(self, user_id: int, themes: str) -> User:
        user = self.get_by_id(user_id)
        user.themes = themes
        self.db.commit()
        self.db.refresh(user)
        return user
