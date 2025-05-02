from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)


class MessageRead(Base):
    __tablename__ = "message_reads"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"), primary_key=True)
    read_at = Column(DateTime(timezone=True), server_default=func.now())
