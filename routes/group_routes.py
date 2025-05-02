from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user
from models import User, Group, Message
from schemas.models import GroupCreate, GroupOut, AddUserToGroup, RemoveUserFromGroup, MessageOut
from services import group_service

router = APIRouter()


@router.post("/create", response_model=GroupOut)
def create_group(
    data: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return group_service.create_group(data, db, current_user.id)


@router.post("/{group_id}/add_user")
def add_user_to_group(
    group_id: int,
    data: AddUserToGroup,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return group_service.add_user_to_group(
        group_id=group_id,
        user_id=data.user_id,
        requester_id=current_user.id,
        db=db
    )


@router.post("/{group_id}/remove_user")
def remove_user_from_group(
    group_id: int,
    data: RemoveUserFromGroup,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return group_service.remove_user_from_group(
        group_id=group_id,
        user_id=data.user_id,
        requester_id=current_user.id,
        db=db
    )


@router.post("/{group_id}/leave")
def leave_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return group_service.leave_group(group_id, current_user.id, db)


@router.get("/groups/{group_id}/history", response_model=list[MessageOut])
def get_group_history(
    group_id: int,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if current_user not in group.members:
        raise HTTPException(status_code=403, detail="Вы не участник группы")

    messages = (
        db.query(Message)
        .filter(Message.chat_id == group_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return messages
