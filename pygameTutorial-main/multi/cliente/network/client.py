import websocket
import threading
import json
import queue

class NetworkClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.message_queue = queue.Queue()
        self.connected = False

    def connect(self):
        def on_open(ws): 
            self.connected = True
            print("✅ Conectado al servidor WebSocket")
        def on_message(ws, message): self.message_queue.put(json.loads(message))
        def on_error(ws, error): print(f"❌ Error de red: {error}")
        def on_close(ws, close_status_code, close_msg): 
            print("🔌 Desconectado del servidor")
            self.connected = False

        self.ws = websocket.WebSocketApp(self.url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def send(self, data):
        if self.connected: self.ws.send(json.dumps(data))

    def get_messages(self):
        messages = []
        while not self.message_queue.empty(): messages.append(self.message_queue.get())
        return messages
