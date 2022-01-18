from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import fastapi.security as security

import sql_app.models as model
import sql_app.schemas as schema
import sql_app.database as database
import sql_app.services as services
import sql_app.crud as crud
from WebSocket.connection import manager, generate_id

# source ./venv/bin/activate && uvicorn main:app --reload
# ./venv/Scripts/activate && uvicorn main:app --reload
# ./venv/Scripts/activate; uvicorn main:app --reload

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


@app.post("/users/")
async def create_user(user: schema.User):
    db_user = await crud.get_user_by_nick(nick=user.nickname)

    if db_user != None:
        raise HTTPException(status_code=400, detail="Nick already registered")

    db_user = await crud.create_user(user=user)
    token = await services.create_token(db_user)
    # return db_user
    return token


@app.post("/messages/users", response_model=model.Message)
async def create_message_for_user(message: schema.Message, user: schema.User = Depends(services.get_current_user)):
    res = await crud.create_user_message(message=message)
    if res == None:
        raise HTTPException(status_code=400, detail="User doesn't exists")
    return res


@app.get("/users/all", response_model=List[schema.User])
async def read_users(user: schema.User = Depends(services.get_current_user)):
    users = await crud.get_users()
    return users


@app.get("/users/", response_model=schema.User)
async def read_user(user_id: Optional[int] = None, user_nick: Optional[str] = None, user: schema.User = Depends(services.get_current_user)):

    if (user_id is None) and (user_nick is not None):
        return await crud.get_user_by_nick(nick=user_nick)

    elif (user_nick is None) and (user_id is not None):
        return await crud.get_user(user_id=user_id)

    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/users/me", response_model=schema.User)
async def read_user(user: schema.User = Depends(services.get_current_user)):
    return user


@app.get("/messages/", response_model=List[model.Message])
async def read_messages(user: schema.User = Depends(services.get_current_user)):
    messages = await crud.get_messages()
    return messages


@app.websocket("/ws/")
# async def websocket_endpoint(websocket: WebSocket, client_id: str = generate_id()):
async def websocket_endpoint(websocket: WebSocket, client_id: str = Depends(generate_id)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, websocket)

    except WebSocketDisconnect:

        manager.disconnect(websocket)


@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = Depends()
):
    user = await services.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user)
