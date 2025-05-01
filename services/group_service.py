from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User
from models.group import Group
from schemas.models import GroupCreate


def create_group(data: GroupCreate, db: Session, creator_id: int):
    group = Group(name=data.name, creator_id=creator_id)
    db.add(group)
    db.flush()

    participant_ids = set(data.participants)
    participant_ids.add(creator_id)

    users = db.query(User).filter(User.id.in_(participant_ids)).all()
    group.members = users

    db.commit()
    db.refresh(group)

    return group


def add_user_to_group(group_id: int, user_id: int, requester_id: int, db: Session):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if group.creator_id != requester_id:
        raise HTTPException(status_code=403, detail="Только создатель может добавлять участников")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user in group.members:
        raise HTTPException(status_code=400, detail="Пользователь уже в группе")

    group.members.append(user)
    db.commit()

    return {"detail": f"Пользователь {user_id} добавлен в группу {group_id}"}


def remove_user_from_group(group_id: int, user_id: int, requester_id: int, db: Session):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if group.creator_id != requester_id:
        raise HTTPException(status_code=403, detail="Только создатель может удалять участников")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user not in group.members:
        raise HTTPException(status_code=400, detail="Пользователь не является участником группы")

    group.members.remove(user)
    db.commit()

    return {"detail": f"Пользователь {user_id} удалён из группы {group_id}"}


def leave_group(group_id: int, user_id: int, db: Session):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user not in group.members:
        raise HTTPException(status_code=400, detail="Вы не участник этой группы")

    group.members.remove(user)
    db.commit()

    return {"detail": f"Пользователь {user_id} вышел из группы {group_id}"}
