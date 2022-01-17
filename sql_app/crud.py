from typing import Optional, List
import ormar
from . import models, schemas
from WebSocket.connection import manager

# print('', flush = True)

# getters


async def get_user(user_id: int):
    res: Optional[models.User] = await models.User.objects.get_or_none(id=user_id)
    print(f'\n\nget user by id\ntype: {type(res)}\n\n')
    return res


async def get_user_by_nick(nick: str):
    res: Optional[models.User] = await models.User.objects.get_or_none(nickname=nick)
    print(f'\n\nget user by nick\ntype: {type(res)}\n\n')
    return res


async def get_users(skip: int = 0, limit: int = 100):
    res: List[Optional[models.User]] = await models.User.objects.all()
    print(f'\n\nget all users\ntype: {type(res)}\n\n')
    return res


async def get_messages(skip: int = 0, limit: int = 100):
    res: List[Optional[models.Message]] = await models.Message.objects.all()
    print(f'\n\nget all messages\ntype: {type(res)}\n\n')
    return res


# creators
async def create_user(user: schemas.User):
    res = await models.User.objects.create(nickname=user.nickname, password=user.password)
    print(f'\n\ncreate user\ntype: {type(res)}\n\n')
    return res


async def create_user_message(message: schemas.Message):
    user: Optional[models.User] = await get_user(message.owner_id)

    if user == None:
        return None
    res: models.Message = await models.Message.objects.create(content=message.content, owner=user)
    print(f'\n\ncreate message\ntype: {type(res)}\n\n')
    return res
