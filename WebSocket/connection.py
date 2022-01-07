from typing import List
from fastapi import WebSocket
from datetime import datetime


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f'{len(self.active_connections)} connections')

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f'{len(self.active_connections)} connections')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message, websocket: WebSocket):
        print(f'broadcast', flush=True)
        cont = 0
        for connection in self.active_connections:
            print(f'for do broadcast', flush=True)
            if connection is not websocket and connection is not self:
                cont = cont + 1
                print(f'cont: {cont}\nvai enviar\n{message}\n', flush=True)
                await connection.send_text(message)


def generate_id():
    d = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    # dd = filter(f, d)
    aux = d.split(' ')
    aux = ''.join(str(it) for it in aux)

    aux = aux.split('/')
    aux = ''.join(str(it) for it in aux)

    aux = aux.split(':')
    aux = ''.join(str(it) for it in aux)
    id = aux
    print(f'{d}', flush=True)
    print(id, flush=True)

    return id


manager = ConnectionManager()
