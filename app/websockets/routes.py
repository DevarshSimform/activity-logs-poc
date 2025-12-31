from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.database.database import SessionLocal
from app.websockets.manager import admin_ws_manager
from app.api.deps import get_current_admin_from_ws

router = APIRouter()

@router.websocket("/ws/admin/activity")
async def admin_activity_ws(
    websocket: WebSocket,
):
    print("🔥 WS endpoint hit")
    await websocket.accept()
    print("✅ WS accepted")

    db = SessionLocal()

    try:
        admin = await get_current_admin_from_ws(websocket, db)
        print("🧑 Admin authenticated:", admin.email)
        await admin_ws_manager.connect(websocket)
        print(f"🟢 WS added | total={len(admin_ws_manager.active)}")
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        admin_ws_manager.disconnect(websocket)
        print("🔴 Admin WebSocket disconnected")
    except Exception as e:
        print("❌ WS error:", e)
    finally:
        db.close()
