from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies import get_current_user_ws
from models import Group, Message, User
from datetime import datetime
from typing import Dict, List

from models.message import MessageRead

router = APIRouter()

active_group_connections: Dict[int, List[WebSocket]] = {}


@router.websocket("/ws/group/{group_id}")
async def group_chat_websocket(
    websocket: WebSocket,
    group_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_ws)
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    if user not in group.members:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    if group_id not in active_group_connections:
        active_group_connections[group_id] = []
    active_group_connections[group_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "message")

            if msg_type == "mark_as_read":
                message_ids = data.get("message_ids", [])
                for mid in message_ids:
                    exists = db.query(MessageRead).filter_by(user_id=user.id, message_id=mid).first()
                    if not exists:
                        db.add(MessageRead(user_id=user.id, message_id=mid))
                db.commit()

                # Проверка, все ли участники прочитали
                for mid in message_ids:
                    msg = db.query(Message).filter_by(id=mid).first()
                    if not msg:
                        continue

                    group = db.query(Group).filter(Group.id == msg.chat_id).first()
                    if not group:
                        continue

                    read_count = db.query(MessageRead).filter(MessageRead.message_id == mid).count()
                    total_users = len(group.members)

                    if read_count == total_users:
                        for conn in active_group_connections.get(group.id, []):
                            await conn.send_json({
                                "type": "read_all",
                                "message_id": mid
                            })

            elif msg_type == "message":
                content = data.get("content")
                if not content:
                    continue

                msg = Message(
                    chat_id=group_id,
                    sender_id=user.id,
                    content=content,
                    timestamp=datetime.utcnow()
                )
                db.add(msg)
                db.commit()

                response = {
                    "type": "message",
                    "chat_id": group_id,
                    "sender_id": user.id,
                    "content": content,
                    "timestamp": str(msg.timestamp)
                }

                for conn in active_group_connections[group_id]:
                    await conn.send_json(response)

    except WebSocketDisconnect:
        active_group_connections[group_id].remove(websocket)
