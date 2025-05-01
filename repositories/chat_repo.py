from sqlalchemy import func
from sqlalchemy.orm import Session

from models.chat import Chat, ChatType
from models.chat_participant import ChatParticipant


def get_private_chat_between_users(db: Session, user1_id: int, user2_id: int):
    subquery = (
        db.query(Chat.id)
        .join(ChatParticipant)
        .filter(Chat.type == ChatType.private)
        .group_by(Chat.id)
        .having(
            func.count(ChatParticipant.user_id.distinct()) == 2,
            func.bool_and(ChatParticipant.user_id.in_([user1_id, user2_id]))
        )
        .subquery()
    )

    return db.query(Chat).filter(Chat.id.in_(subquery)).first()


def create_private_chat(db: Session, user1_id: int, user2_id: int) -> Chat:
    chat = Chat(type=ChatType.private)
    db.add(chat)
    db.flush()

    db.add_all([
        ChatParticipant(chat_id=chat.id, user_id=user1_id),
        ChatParticipant(chat_id=chat.id, user_id=user2_id)
    ])
    db.commit()
    db.refresh(chat)
    return chat
