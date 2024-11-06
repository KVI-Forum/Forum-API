from fastapi import APIRouter, Request, Form, Header, HTTPException, Depends, Cookie
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import user_service, category_service
from data.models import User,UserRegistration

users_router = APIRouter(prefix='/users')
access_router = APIRouter(prefix='/admin')
templates = CustomJinja2Templates(directory='templates')

def admin_required(token: str = Cookie(None)):
    if not token or not user_service.is_admin(token):
        raise HTTPException(status_code=403, detail="Admin access required.")
    return token

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


@access_router.get('/manage-access')
def access_management(request: Request, token: str = Depends(admin_required)):
    user_id = int(token.split(";")[0])
    categories = category_service.get_all(user_id, token)
    users = user_service.all_users()

    return templates.TemplateResponse("access_management.html", {
        "request": request,
        "categories": categories,
        "users": users,
        "token": token
    })


@access_router.post('/users/{user_id}/category/read')
def grant_read_access(user_id: int, category_id: int = Form(...), token: str = Form(...)):
    if user_service.is_admin(token):
        # remind to explain this line why True or int
        if user_service.give_read_access(user_id, category_id)== True or int:
            return {"message": f"Read access granted to user {user_id} for category {category_id}"}
    raise HTTPException(status_code=400, detail="Failed to grant read access")


@access_router.post('/users/{user_id}/category/write')
def grant_write_access(user_id: int, category_id: int = Form(...), token: str = Form(...)):
    if user_service.is_admin(token):
        # remind to explain this line why True or int
        if user_service.give_write_access(user_id, category_id) == True or int:
            return {"message": f"Write access granted to user {user_id} for category {category_id}"}
    raise HTTPException(status_code=400, detail="Failed to grant write access")


@access_router.post('/users/{user_id}/category/revoke')
def revoke_access(user_id: int, category_id: int = Form(...), token: str = Form(...)):
    if user_service.is_admin(token):
        if user_service.revoke_access(user_id, category_id):
            return {"message": f"Access revoked from user {user_id} for category {category_id}"}
    raise HTTPException(status_code=400, detail="Failed to revoke access")


