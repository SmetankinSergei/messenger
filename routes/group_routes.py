from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user
from models import User
from schemas.models import GroupCreate, GroupOut, AddUserToGroup, RemoveUserFromGroup
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
