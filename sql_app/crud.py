from typing import Optional
import ormar
from . import models, schemas

# print('', flush = True)
#getters
async def get_user(user_id: int):
    #return db.query(models.User).filter(models.User.id == user_id).first()
    res: models.User | None = await models.User.objects.get_or_none(id == user_id)
    print('usou get_user pelo id:\n{}\n'.format(res), flush = True)
    return res


async def get_user_by_nick(nick: str):
    # var = db.query(models.User).filter(models.User.nickname == nick).first()
    res: models.User | None = await models.User.objects.get_or_none(nickname == nick)
    print('usou get_user pelo nick:\n{}\n'.format(res), flush = True)
    return res


async def get_users(skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    res: List[Optional[models.User]] = await models.User.objects.all()
    print('buscou todos os usuarios:\n{}\n'.format(res), flush = True)
    return res


async def get_messages(skip: int = 0, limit: int = 100):
    # return db.query(models.Message).offset(skip).limit(limit).all()
    res: List[Optional[models.Message]] = await models.Message.objects.all()
    print('buscou todas as mensagens:\n{}\n'.format(res), flush = True)
    return res


#creators
async def create_user(user: schemas.User):
    db_user = models.User(nickname=user.nickname, password=user.password)
    res: models.User | None = await db_user.save()
    print('criou um usuario:\n{}\n'.format(res), flush = True)
    return res


async def create_user_message(message: schemas.Message):
    db_message = models.Message(content = message.content, owner_id = message.owner_id)
    res: models.Message | None = await db_message.save()
    print('criou uma mensagem:\n{}\n'.format(res), flush = True)
    return res