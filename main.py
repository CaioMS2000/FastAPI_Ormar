from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

import sql_app.models as model
import sql_app.schemas as schema
import sql_app.database as database
import sql_app.crud as crud
from WebSocket.connection import manager

# source ./venv/bin/activate && uvicorn main:app --reload
# ./venv/Scripts/activate && uvicorn main:app --reload
# Response Model
# skiped: CORS; Bigger Applications - Multiple Files

# model.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.metadata.create_all(database.engine)
app.state.database = database.database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.post("/users/", response_model=schema.User)
async def create_user(user: schema.User):
    db_user = await crud.get_user_by_nick(nick=user.nickname)

    if db_user != None:
        raise HTTPException(status_code=400, detail="Nick already registered")

    return await crud.create_user(user=user)


@app.post("/messages/users", response_model=model.Message)
async def create_message_for_user(message: schema.Message):
    res = await crud.create_user_message(message=message)
    if res == None:
        raise HTTPException(status_code=400, detail="User doesn't exists")
    return res


@app.get("/users/all", response_model=List[schema.User])
async def read_users(skip: int = 0, limit: int = 100):
    users = await crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/", response_model=schema.User)
async def read_user(user_id: Optional[int] = None, user_nick: Optional[str] = None):
    if (user_id is None) and (user_nick is not None):
        return await crud.get_user_by_nick(nick=user_nick)

    elif (user_nick is None) and (user_id is not None):
        return await crud.get_user(user_id=user_id)

    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/messages/", response_model=List[model.Message])
async def read_messages(skip: int = 0, limit: int = 100):
    messages = await crud.get_messages(skip=skip, limit=limit)
    return messages


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")

    except WebSocketDisconnect:

        manager.disconnect(websocket)

        await manager.broadcast(f"Client #{client_id} left the chat")
