from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user
from models.user import User
from services import chat_service

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

