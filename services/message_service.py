from repositories import message_repo


def get_chat_history(chat_id: int, limit: int, offset: int, db):
    return message_repo.get_messages(chat_id, limit, offset, db)
