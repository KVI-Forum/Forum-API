from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates
from services import category_service

categories_router = APIRouter(prefix='/categories')
templates = CustomJinja2Templates(directory='templates')

@categories_router.get('/')
def categories(request: Request):
    categories = category_service.get_all()
    return templates.TemplateResponse(request=request, name='categories.html',context = categories)