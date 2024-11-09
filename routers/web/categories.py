from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import category_service,topic_service,user_service

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
        category = category_service.get_by_id_public(id)
    else:
        user_id = int(token.split(';')[0])
        category = category_service.get_by_id(id, user_id, token)
    
    if not category:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Category not found"})
    
    return templates.TemplateResponse("category.html", {"request": request, "category": category, "topics": topics})

@categories_router.post('/{id}/locked')
def lock_category(request : Request ,id: int, token: str = Form(...)):
    user_id = int(token.split(";")[0])
    locked_cat = category_service.lock(id)
    if not locked_cat:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Category not found"})
    return RedirectResponse(f'/categories',status_code=302)

@categories_router.post('/{id}/unlocked')
def unlock_category(request : Request , id: int, token: str = Form(...)):
    user_id = int(token.split(";")[0])
    unlocked_cat = category_service.unlock(id)
    if not unlocked_cat:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Category not found"})
    return RedirectResponse(f'/categories',status_code=302)

@categories_router.post('/{category_id}/topics')
def post_topic(
    category_id: int,
    request: Request,
    name: str = Form(...),
    author_id: int = Form(...),
    token: str = Form(...)
    ):
    
    topic_id = topic_service.create(name,category_id,author_id,token)
    
    if topic_id:
        return RedirectResponse(f'/categories/{category_id}',status_code=302)
    else:
        return templates.TemplateResponse("fail.html", {"request": request})
    
@categories_router.get('/{category_id}/priviliged')
def get_priviliged_users(request: Request, category_id: int):
    token = request.cookies.get('token')
    user_id = int(token.split(';')[0])
    category = category_service.get_by_id(category_id,user_id,token)
    users = user_service.get_privileged_users_by_category(category_id)
    return templates.TemplateResponse("priviliged_users.html", {"request": request, "users": users, "category": category})