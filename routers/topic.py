from fastapi import APIRouter, Response, Header

from common.auth import get_user_or_raise_401, verify_authenticated_user
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
def create_topic(topic: Topic,token:str= Header()):

    verify_authenticated_user(token)
    topic_id = topic_service.create(topic.name,topic.categories_id)
    if topic_id:
        return Response(status_code=200,content=f"topic with id:{topic_id} and name:'{topic.name}' was created.")
    else:
        return Response(status_code=404, content="Category not found.")




