from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates
from services import category_service,topic_service

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

@categories_router.get('/{id}')
def get_category_by_id(request: Request, id: int):
    token = request.cookies.get('token')
    topics = topic_service.get_by_category_id(id)
    
    if not token:
        categories = category_service.get_by_id_public(id)
    else:
        user_id = int(token.split(';')[0])
        categories = category_service.get_by_id(id, user_id, token)
    
    if not categories:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Category not found"})
    
    category = categories
    return templates.TemplateResponse("category.html", {"request": request, "category": category, "topics": topics})

