from unicodedata import category

from fastapi import APIRouter, Response, Header

from common.auth import verify_admin
from data.models import LoginData
from routers.category import get_category_by_id
from services import user_service, category_service
from data.models import User , UserRegistration
from services.user_service import get_user_by_id, give_read_access, give_write_access, revoke_access, \
    get_privileged_users_by_category

users_router = APIRouter(prefix='/users')

#todo
@users_router.post('/login')
def login(data: LoginData):
    user = user_service.try_login(data.username, data.password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=401, content="Invalid login data")
    


@users_router.post('/register')
def register(data: UserRegistration):

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        password=data.password,
        email=data.email
    ) 
    user = user_service.create_user(user)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=400, content=f'Username or Email is taken.')

from fastapi import HTTPException, Response

@users_router.patch("/read_access/{user_id}/category/{category_id}")
def read_access(user_id: int, category_id: int, token: str = Header()):
    user_data = get_user_by_id(user_id)
    category_data = category_service.get_by_id(category_id, user_id, token)

    if not user_data or not category_data:
        return Response(status_code=404, content="Category or user not found.")

    verify_admin(token)

    access_granted = give_read_access(user_id, category_id)
    if access_granted:
        return Response(status_code=200, content="Read access granted successfully.")
    else:
        return Response(status_code=500, content="Failed to grant read access.")

@users_router.patch("/write_access/{user_id}/category/{category_id}")
def write_access(user_id: int, category_id: int, token: str = Header()):
    user_data = get_user_by_id(user_id)
    category_data = category_service.get_by_id(category_id, user_id, token)

    if not user_data or not category_data:
        return Response(status_code=404, content="Category or user not found.")

    verify_admin(token)

    access_granted = give_write_access(user_id, category_id)
    if access_granted:
        return Response(status_code=200, content="Write access granted successfully.")
    else:
        return Response(status_code=500, content="Failed to grant write access.")

@users_router.patch("/revoke_access/{user_id}/category/{category_id}")
def revoke_access_endpoint(user_id: int, category_id: int, token: str = Header()):
    user_data = get_user_by_id(user_id)
    category_data = category_service.get_by_id(category_id, user_id, token)

    if not user_data or not category_data:
        return Response(status_code=404, content="Category or user not found.")


    try:
        verify_admin(token)
    except HTTPException:
        return Response(status_code=401, content="Unauthorized access.")


    access_revoked = revoke_access(user_id, category_id)
    if access_revoked:
        return Response(status_code=200, content="Access revoked successfully.")
    else:
        return Response(status_code=404, content="No access found to revoke.")


@users_router.get("/privileged_users/{category_id}")
def view_privileged_users(category_id: int, token: str = Header()):

    try:
        verify_admin(token)
    except HTTPException:
        return Response(status_code=401, content="Unauthorized access.")

    users_data = get_privileged_users_by_category(category_id)


    users_by_category = {}

    for username, access_type in users_data:
        if username not in users_by_category:
            users_by_category[username] = []
        users_by_category[username].append(access_type)


    sorted_categories = sorted(users_by_category.keys())


    formatted_response = []
    for username in sorted_categories:
        formatted_response.append(f"{username}")
        for access in users_by_category[username]:
            if access == 1:
                formatted_response.append(f"---read access"+"\n")
            if access == 2:
                formatted_response.append(f"---write access"+"\n")

    return Response(content="\n".join(formatted_response), media_type="text/plain")