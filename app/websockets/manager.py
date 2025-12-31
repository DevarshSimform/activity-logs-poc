from fastapi import WebSocket


class AdminWebSocketManager:
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        self.active.add(ws)
        print(f"🟢 Admin WS connected | total={len(self.active)}")

    def disconnect(self, ws: WebSocket):
        self.active.discard(ws)
        print(f"🔴 Admin WS disconnected | total={len(self.active)}")

    async def broadcast(self, message: dict):
        print(f"📡 Broadcasting to {len(self.active)} admin sockets")

        if not self.active:
            print("⚠️ No active admin WS connections")
            return

        dead = []

        for ws in self.active:
            try:
                print("➡️ Sending event to admin WS")
                await ws.send_json(message)
            except Exception as e:
                print("❌ WS send failed:", repr(e))
                dead.append(ws)

        for ws in dead:
            self.active.discard(ws)
            print(f"🧹 Removed dead WS | total={len(self.active)}")



admin_ws_manager = AdminWebSocketManager()
