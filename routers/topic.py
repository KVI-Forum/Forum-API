from fastapi import APIRouter,Response
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
            return topic_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result

@topic_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if topic is None:
        return Response(status_code=404, content="Topic not found.")
    else:
        return topic

