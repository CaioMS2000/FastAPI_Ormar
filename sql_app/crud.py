from typing import Optional, List
import ormar
from . import models, schemas
import services.user as S_user

# print('', flush = True)
# getters


async def get_user(user_id: int):
    # return db.query(models.User).filter(models.User.id == user_id).first()
    res: models.User | None = await models.User.objects.get_or_none(id= user_id)
    print('usou get_user pelo id:\n{}\n'.format(res), flush=True)
    return res


async def get_user_by_nick(nick: str):
    # var = db.query(models.User).filter(models.User.nickname == nick).first()
    res: models.User | None = await models.User.objects.get_or_none(nickname= nick)
    print('usou get_user pelo nick:\n{}\n'.format(res), flush=True)
    return res


async def get_users(skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    res: List[Optional[models.User]] = await models.User.objects.all()
    print('buscou todos os usuarios:\n{}\n'.format(res), flush=True)
    return res


async def get_messages(skip: int = 0, limit: int = 100):
    # return db.query(models.Message).offset(skip).limit(limit).all()
    res: List[Optional[models.Message]] = await models.Message.objects.all()
    print('buscou todas as mensagens:\n{}\n'.format(res), flush=True)
    return res


# creators
async def create_user(user: schemas.User):
    # res: models.User | None = await models.User.obsjects.create(nickname=user.nickname, password=user.password)
    print('entrou na criação\n', flush=True)
    res = await models.User.objects.create(nickname=user.nickname, password=user.password)
    print('criou um usuario:\n{}\n'.format(res), flush=True)
    return res


async def create_user_message(message: schemas.Message):
    user = await get_user(message.owner_id)
    print(f'usuario usado na criação da mensagem\n{user}\n#\n')
    # res: models.Message | None = await models.Message.objects.create(content=message.content, owner=user)
    res = await models.Message.objects.create(content=message.content, owner=user)
    print('criou uma mensagem:\n{}\n'.format(res), flush=True)
    return res
