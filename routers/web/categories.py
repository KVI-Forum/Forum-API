from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates
from services import category_service

categories_router = APIRouter(prefix='/categories')
templates = CustomJinja2Templates(directory='templates')

@categories_router.get('/')
def categories(request: Request):
    token = request.cookies.get('token')
    if not token:
        categories = category_service.get_all_public()
    else:
        user_id = int(token.split(';')[0])
        categories = category_service.get_all(user_id,token)

   
    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories})
