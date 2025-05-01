from sqlalchemy.orm import Session

from repositories import message_repo
from models import Message
from typing import List


def get_chat_history(chat_id: int, limit: int, offset: int, db):
    return message_repo.get_messages(chat_id, limit, offset, db)


async def mark_messages_as_read(chat_id: int, reader_id: int, db: Session, connections: List):
    unread = (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .filter(Message.sender_id != reader_id)
        .filter(Message.is_read == False)
        .all()
    )

    if not unread:
        return

    message_ids = [msg.id for msg in unread]

    for msg in unread:
        msg.is_read = True

    db.commit()

    for conn in connections:
        await conn.send_json({
            "type": "read",
            "reader_id": reader_id,
            "message_ids": message_ids
        })
