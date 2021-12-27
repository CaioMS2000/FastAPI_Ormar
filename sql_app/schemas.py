from datetime import date, datetime
from pydantic import BaseModel
from typing import List, Optional

class MessageBase(BaseModel):
    id: int = 0
    sent_date: datetime = datetime.now()
    num_char: int = 0
    deleted: bool = False


class Message(MessageBase):
    content: str
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: int = 0
    nick_color: str = '#000000'
    num_msg: int = 0
    reg_date: datetime = datetime.now()
    messages: List[Message] = []    



class User(UserBase):
    password: str
    nickname: str
    
    class Config:
        orm_mode = True