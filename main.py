from fastapi import Depends, FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

import sql_app.models as model
import sql_app.schemas as schema
import sql_app.database as database
import sql_app.crud as crud


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
def create_user(user: schema.User):
    db_user = crud.get_user_by_nick(nick=user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nick already registered")
    return crud.create_user(user=schema.User(nickname=user.nickname, password=user.password))


@app.post("/messages/users", response_model=schema.Message)
def create_message_for_user(message: schema.Message):
    return crud.create_user_message(message=message)


@app.get("/users/all", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100):
    print('todos', flush=True)
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/", response_model=schema.User)
def read_user(user_id: Optional[int] = None, user_nick: Optional[str] = None):
    if (user_id is None) and (user_nick is not None):
        print("pelo nick", flush=True)
        return read_user_by_nick(user_nick=user_nick)

    elif (user_nick is None) and (user_id is not None):
        print("pelo id", flush=True)
        return read_user_by_id(user_id=user_id)

    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/messages/", response_model=List[schema.Message])
def read_messages(skip: int = 0, limit: int = 100):
    messages = crud.get_messages(skip=skip, limit=limit)
    return messages
