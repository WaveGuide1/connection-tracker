from fastapi.responses import HTMLResponse
from fastapi import FastAPI


app = FastAPI()


# Simple homepage to test WebSocket
@app.get("/")
async def get():
    return HTMLResponse("""
    <html>
        <head>
            <title>Webhook + WS Demo</title>
        </head>
        <body>
            <h1>WebSocket Test</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                const ws = new WebSocket(`ws://${window.location.host}/ws`);
                ws.onmessage = function(event) {
                    const messages = document.getElementById('messages')
                    const message = document.createElement('li')
                    const content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    const input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </body>
    </html>
    """)