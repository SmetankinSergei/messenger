from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from typing import Dict, List
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies import get_current_user_ws
from models import Message, ChatParticipant
from datetime import datetime

router = APIRouter()


active_connections: Dict[int, List[WebSocket]] = {}


@router.websocket("/ws/chat/{chat_id}")
async def chat_websocket(
    websocket: WebSocket,
    chat_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user_ws)
):

    participant = db.query(ChatParticipant).filter_by(
        chat_id=chat_id,
        user_id=user.id
    ).first()

    if not participant:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content:
                continue

            msg = Message(
                chat_id=chat_id,
                sender_id=user.id,
                content=content,
                timestamp=datetime.utcnow()
            )
            db.add(msg)
            db.commit()

            response = {
                "chat_id": chat_id,
                "sender_id": user.id,
                "content": content,
                "timestamp": str(msg.timestamp)
            }

            for conn in active_connections[chat_id]:
                await conn.send_json(response)

    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
