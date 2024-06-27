from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

class ConnectionManager:

    def __init__(self) -> None:
        self.connections : list[WebSocket] = []

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket : WebSocket):
        self.connections.remove(websocket)

    async def send_personal_messsage(self, message : str, websocket : WebSocket):
        await websocket.send_json({})

    async def broadcast(self, user : str, message : str):
        for connection in self.connections:
            await connection.send_json({'user' : user, "message" : message})

rooms = {}

@app.websocket("/ws/{room_id}/{username}")
async def websocket_endpoint(websocket: WebSocket, room_id:str, username:str):
    if room_id not in rooms:
        room_manager = ConnectionManager()
        rooms[room_id] = room_manager
    
    manager = rooms[room_id]
    await manager.connect(websocket)
    await manager.broadcast(username, f"Joined the Room")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(username, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(username, f"Left the Room")

