from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ========================= USERS ========================= #
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


# ========================= CHATS ========================= #
class ChatBase(BaseModel):
    name: Optional[str] = None
    type: str  # "private" или "group"


class ChatCreate(ChatBase):
    pass


class ChatOut(ChatBase):
    id: int

    class Config:
        from_attributes = True


# ========================= GROUPS ========================= #
class GroupBase(BaseModel):
    name: str
    creator_id: int


class GroupCreate(GroupBase):
    participants: List[int]  # ID участников


class GroupOut(GroupBase):
    id: int
    participants: List[int]

    class Config:
        from_attributes = True


# ========================= MESSAGES ========================= #
class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int


class MessageOut(MessageBase):
    id: int
    timestamp: datetime
    sender_id: int
    chat_id: int
    is_read: bool

    class Config:
        from_attributes = True
