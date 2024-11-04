from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates
from services import category_service 

index_router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')

@index_router.get('/')
def index(request: Request):
    token = request.cookies.get('token')
    if not token:
        categories = category_service.get_all_public()
    else:
        user_id = int(token.split(';')[0])
        categories = category_service.get_all(user_id, token)
    
    return templates.TemplateResponse("index.html", {"request": request, "categories": categories})
