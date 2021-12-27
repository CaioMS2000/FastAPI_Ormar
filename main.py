from fastapi import Depends, FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

import sql_app.crud as crud
import sql_app.models as model


#source ./venv/bin/activate && uvicorn main:app --reload
#./venv/Scripts/activate && uvicorn main:app --reload
#Response Model
#skiped: CORS; Bigger Applications - Multiple Files

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_user_by_nick(user_nick: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nick(db, nick = user_nick)
    if db_user is None:
        raise HTTPException(status_code = 404, detail = "User nick not found")
    return db_user


def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code = 404, detail = "User id not found")
    return db_user


# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.post("/users/", response_model=schema.User)
def create_user(user: schema.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_nick(db, nick = user.nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nick already registered")
    return crud.create_user(db=db, user=schema.User(nickname = user.nickname, password = user.password))


@app.post("/messages/users", response_model = schema.Message)
def create_message_for_user(message: schema.Message, db: Session = Depends(get_db)):
    return crud.create_user_message(message = message, db = db)


@app.get("/users/all", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print('todos', flush = True)
    users = crud.get_users(db, skip=skip, limit=limit)    
    return users


@app.get("/users/", response_model=schema.User)
def read_user(user_id: Optional[int] = None, user_nick: Optional[str] = None, db: Session = Depends(get_db)):
    if (user_id is None) and (user_nick is not None):
        print("pelo nick", flush = True)
        return read_user_by_nick(user_nick = user_nick, db = db)

    elif (user_nick is None) and (user_id is not None):
        print("pelo id", flush = True)
        return read_user_by_id(user_id= user_id, db = db)

    else:
        raise HTTPException(status_code = 500, detail = "Internal Server Error")


@app.get("/messages/", response_model=List[schema.Message])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip = skip, limit = limit)
    return messages
