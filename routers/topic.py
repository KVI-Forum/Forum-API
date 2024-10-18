from fastapi import APIRouter, Response, Header

from common.auth import get_user_or_raise_401
from data.models import Topic
from services import topic_service

topic_router = APIRouter(prefix='/topics')

@topic_router.get('/')
def get_topics(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = topic_service.get_all(search)
    if result is None:
        return Response(status_code=404, content="No topics found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return topic_service.sort_topics(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result

@topic_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if topic is None:
        return Response(status_code=404, content="Topic not found.")
    else:
        return topic


@topic_router.post("/")
def create_topic(topic_name,category_name,token:str= Header()):
    user = get_user_or_raise_401(token)
    topic = topic_service.create(topic_name,category_name)
    if topic:
        return Response(status_code=200,content=f"topic with id:{topic} and name:'{topic_name}' created.")
    else:
        return Response(status_code=404, content="Category not found.")




