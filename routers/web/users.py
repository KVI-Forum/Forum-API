from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import user_service
from data.models import User,UserRegistration

users_router = APIRouter(prefix='/users')
templates = CustomJinja2Templates(directory='templates')


@users_router.get('/register')
def serve_register(request:Request):
    return templates.TemplateResponse(request=request, name='register.html')

@users_router.get('/login')
def serve_login(request:Request):
    return templates.TemplateResponse(request=request, name='login.html')

@users_router.post('/register')
def register(request:Request, first_name: str = Form(...), last_name: str = Form(...), username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    user = User(first_name=first_name, last_name=last_name, username=username, password=password, email=email)
    new_user = user_service.create_user(user)

    if new_user:
        token = user_service.create_token(user)
        response = RedirectResponse('/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username or email already exists"})
    
@users_router.post('/login')
def login(request:Request, username: str = Form(...), password: str = Form(...)):
    user = user_service.try_login(username, password)
    if user:
        token = user_service.create_token(user)
        response = RedirectResponse('/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})


@users_router.post('/logout')
def logout():
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie('token')
    return response