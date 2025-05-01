from models import Message


def get_messages(chat_id: int, limit: int, offset: int, db):
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )
