from fastapi import APIRouter,Response
from data.models import LoginData
from services import user_service
from data.models import User

users_router = APIRouter(prefix='/users')


@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=401, content="Invalid login data")
    


@users_router.post('/register')
def register(data: User):
    
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        password=data.password,
        email=data.email
    )  # Notice is_admin is not passed here
    user = user_service.create_user(user)
    
    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=400, content=f'Username {data.username} is taken.')
