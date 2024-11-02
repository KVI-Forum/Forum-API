from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates


about_router = APIRouter(prefix='/about')
templates = CustomJinja2Templates(directory='templates')

@about_router.get('')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='about.html')