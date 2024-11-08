from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates
from services import user_service


messenger_router = APIRouter(prefix='/messenger')
templates = CustomJinja2Templates(directory='templates')


@messenger_router.get('/')
def serve_messenger(request: Request):
    token = request.cookies.get('token')
    user_id = int(token.split(';')[0])
    users = user_service.get_users_except(user_id)
    return templates.TemplateResponse("messenger.html", {"request": request, "users": users})