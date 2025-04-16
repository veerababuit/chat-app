from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]  # Frontend origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = {}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections[username] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            recipient = data["to"]
            message = data["message"]

            if recipient in active_connections:
                await active_connections[recipient].send_json({
                    "from": username,
                    "message": message
                })
    except WebSocketDisconnect:
        if username in active_connections:
            del active_connections[username]
