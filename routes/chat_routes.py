from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user
from models.user import User
from schemas.models import MessageOut
from services import chat_service, message_service

from fastapi import APIRouter


router = APIRouter()


@router.post("/start")
def start_chat(
    interlocutor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if interlocutor_id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя создать чат с самим собой")

    chat = chat_service.get_or_create_chat(current_user.id, interlocutor_id, db)
    return {"chat_id": chat.id}


@router.get("/history/{chat_id}", response_model=list[MessageOut])
def get_chat_history(
    chat_id: int,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    return message_service.get_chat_history(chat_id, limit, offset, db)
