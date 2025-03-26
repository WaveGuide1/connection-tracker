from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
import json
from app.main import manager


app = FastAPI()

# Webhook endpoint for github
@app.post("webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    event_type = request.headers.get("X-GitHub-Event", "ping")

        # Broadcast to all WebSocket clients
    await manager.broadcast(
        json.dumps({
            "event": "github_webhook",
            "type": event_type,
            "data": payload
        })
    )

    return {"status": "success", "event": event_type}


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back and broadcast
            await websocket.send_text(f"Message received: {data}")
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
        