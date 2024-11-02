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