from fastapi import APIRouter,Response
from data.models import Category
from services import category_service


category_router = APIRouter(prefix='/categories')


@category_router.get('/')
def get_categories(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = category_service.get_all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result

    





