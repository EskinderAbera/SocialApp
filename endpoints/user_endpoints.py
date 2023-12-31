from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from db.db import get_session
from models.user_models import User, UserInput, UserLogin
from repos.user_repos import select_all_users, find_user
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201, tags=['users'],
                  description='Register new user')
def register(*, session: Session = Depends(get_session), user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd)
    session.add(u)
    session.commit()
    return JSONResponse({'msg': 'created!'}, status_code=HTTP_201_CREATED)


@user_router.post('/login', tags=['users'])
def login(user: UserLogin):
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@user_router.get('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user
