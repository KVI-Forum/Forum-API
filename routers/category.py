from email.header import Header

from fastapi import APIRouter,Response

from common.auth import verify_admin
from data.models import Category
from services import category_service
from services.user_service import is_admin

#TODO connect toppics to categories // SHOULD task (admin creates category)
category_router = APIRouter(prefix='/categories')


@category_router.get('')
def get_categories(sort: str | None = None, sort_by: str | None = None, token: str = Header()):
    user_id = token.split(";")[0]

    result = category_service.get_all(user_id=user_id,token=token)
    if result is None:
        return Response(status_code=404, content="No categories found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return category_service.sort_categories(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result
        




@category_router.get('/{id}')
def get_category_by_id(id: int, token: str = Header()):
    user_id = token.split(";")[0]
    category = category_service.get_by_id(id, user_id,token)

    if category is None:
        return Response(status_code=404, content="Category not found.")
    else:
        return category
    
@category_router.post('')
def create_category(category: Category,token:str=Header()):
    user_id = token.split(";")[0]
    verify_admin(token)
    category_id = category_service.create(category.name, category.description)
    if category_id:
        return Response(status_code=200, content=f"Category with id: {category_id} and name: '{category.name}' was created.")
    else:
        return Response(status_code=401, content="Category with that name already exists.")

@category_router.put('/{id}')
def update_access(id: int, category: Category, token: str = Header()):
    user_id = token.split(";")[0]
    category_data = category_service.get_by_id(id,user_id,token)
    
    if category_data is None:
        return Response(status_code=404, content="Category not found.")
    
    verify_admin(token)

    if category_data and len(category_data) > 0:
        category_id = category_data[0]['category_id']
        
        if category_service.update_access(category_id, category.private):
            return Response(status_code=200, content=f"Category with id: {category_id} was updated.")
    
    
