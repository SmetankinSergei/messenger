from sqlalchemy import Column, Integer, String, Enum
from db.database import Base
import enum


class ChatType(str, enum.Enum):
    private = "private"
    group = "group"


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    type = Column(Enum(ChatType), default=ChatType.private)
