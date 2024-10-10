from fastapi import APIRouter,Response
from data.models import Category
from services import category_service

#TODO connect toppics to categories // SHOULD task (admin creates category)
category_router = APIRouter(prefix='/categories')


@category_router.get('/')
def get_categories(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = category_service.get_all(search)
    if result is None:
        return Response(status_code=404, content="No categories found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return category_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result
        




@category_router.get('/{id}')
def get_category_by_id(id: int):
    category = category_service.get_by_id(id)

    if category is None:
        return Response(status_code=404, content="Category not found.")
    else:
        return category
    





