from sqlalchemy.orm import Session

from models.chat import Chat
from repositories import chat_repo


def get_or_create_chat(user1_id: int, user2_id: int, db: Session) -> Chat:
    existing = chat_repo.get_private_chat_between_users(db, user1_id, user2_id)
    if existing:
        return existing
    return chat_repo.create_private_chat(db, user1_id, user2_id)
