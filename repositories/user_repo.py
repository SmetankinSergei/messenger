from sqlalchemy.orm import Session
from models.user import User


def save_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
