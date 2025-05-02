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


class GroupCreate(BaseModel):
    name: str
    participants: List[int]


class GroupOut(GroupBase):
    id: int
    participants: List[int]

    class Config:
        from_attributes = True


class AddUserToGroup(BaseModel):
    user_id: int


class RemoveUserFromGroup(BaseModel):
    user_id: int


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


class MessageReadBase(BaseModel):
    message_id: int


class MessageReadCreate(MessageReadBase):
    pass


class MessageReadOut(MessageReadBase):
    user_id: int
    read_at: datetime

    class Config:
        from_attributes = True