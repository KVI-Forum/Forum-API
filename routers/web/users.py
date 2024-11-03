from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import user_service

users_router = APIRouter(prefix='/users')
templates = CustomJinja2Templates(directory='templates')


@users_router.get('/register')
def serve_register(request:Request):
    return templates.TemplateResponse(request=request, name='register.html')

@users_router.get('/login')
def serve_login(request:Request):
    return templates.TemplateResponse(request=request, name='login.html')

@users_router.post('register')
def register(request:Request, username: str = Form(...), password: str = Form(...)):
    user = user_service.create_user(username, password)
    if user:
        token = user_service.create_token(user)
        response = RedirectResponse('/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name='register.html', context={'error': 'Username taken!'})
    
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