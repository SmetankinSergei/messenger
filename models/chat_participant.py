from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    chat = relationship("Chat", backref="participants")
    user = relationship("User", backref="chats")
