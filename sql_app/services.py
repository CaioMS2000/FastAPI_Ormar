import jwt
import fastapi.security as security
from fastapi import Depends, HTTPException

from . import models, schemas, crud

JWT_SECRET = "myjwtsecret"
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")
# print('', flush = True)


async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)

    obj = {"id": user_obj.id, "nick_color": user_obj.nick_color,
           "num_msg": user_obj.num_msg, "reg_date": user_obj.reg_date.strftime("%m%d%Y%H%M%S"),
           "messages": user_obj.messages, "password": user_obj.password, "nickname": user_obj.nickname}

    # token = jwt.encode(user_obj.dict(), JWT_SECRET)
    token = jwt.encode(obj, JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def authenticate_user(nick: str, password: str):
    user = await crud.get_user_by_nick(nick)

    if not user:
        return False

    if user.password != password:
        return False

    return user


# async def get_current_user(token: str = Depends(oauth2schema)):
async def get_current_user(token=Depends(oauth2schema)):
    # try:
    #     payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    #     user = db.query(_models.User).get(payload["id"])
    # except:
    #     raise _fastapi.HTTPException(
    #         status_code=401, detail="Invalid Email or Password"
    #     )

    # return _schemas.User.from_orm(user)
    payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    user = await crud.get_user(payload["id"])

    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid Email or Password")

    return schemas.User.from_orm(user)
