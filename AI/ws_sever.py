from websocket_server import WebsocketServer
import threading

server = None
clients = []

def new_client(client, server_):
    clients.append(client)
    print("FE connected:", client["id"])

def start_ws():
    global server
    server = WebsocketServer(host="0.0.0.0", port=8765)
    server.set_fn_new_client(new_client)
    print("WebSocket running at ws://localhost:8765")
    server.run_forever()

def send_data(msg):
    if server is None:
        return
    for c in clients:
        server.send_message(c, msg)

def run_ws_background():
    threading.Thread(target=start_ws, daemon=True).start()
