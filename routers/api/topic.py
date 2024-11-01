from fastapi import APIRouter, Response, Header, HTTPException

from common.auth import get_user_or_raise_401, verify_authenticated_user, verify_admin
from data.models import Topic
from services import topic_service
from services.topic_service import exists

topic_router = APIRouter(prefix='/api/topics')

@topic_router.get('')
def get_topics(token:str ,sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    result = topic_service.get_all(user_id,search)
    if result is None:
        return Response(status_code=404, content="No topics found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return topic_service.sort_topics(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result

@topic_router.get('/{id}')
def get_topic_by_id(token:str, id: int):
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    topic_check = exists(id)
    if not topic_check:
        return Response(status_code=404, content="Topic not found.")

    topic = topic_service.get_by_id(id,user_id)
    if topic is None:
        return Response(status_code=401, content="you can't see this topic bro, sorry!")
    else:
        return topic


@topic_router.post("")
def create_topic(topic: Topic,token:str= Header()):
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    topic_id = topic_service.create(topic.name,topic.categories_id,user_id,token)
    if topic_id:
        return Response(status_code=200,content=f"topic with id: {topic_id} and name: '{topic.name}' was created.")
    else:
        return Response(status_code=404, content="Category not found or locked.")
    
@topic_router.patch("/{topic_id}/best_reply/{reply_id}")
def update_best_reply(id: int, reply_id: int,token:str= Header()):
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    topic = topic_service.exists(id)
    if topic is None:
        return Response(status_code=404, content="Topic not found.")
    else:
        update = topic_service.update_best_reply(id, reply_id, user_id)
        if update is False:
            return Response(status_code=401, content="You are not the author of the topic.")

        return Response(status_code=200, content="Best reply updated.")

@topic_router.patch("/{id}/locked")
def lock_topic(id: int, token:str= Header()):
    try:
        verify_admin(token)
    except HTTPException:
        return Response(status_code=401, content="Unauthorized access.")

    result = topic_service.lock(id)
    if result is False:
        return Response(status_code=404, content="Topic not found.")
    return Response(status_code=200, content="Topic locked.")

@topic_router.patch("/{id}/unlocked")
def unlock_topic(id: int, token:str= Header()):
    try:
        verify_admin(token)
    except HTTPException:
        return Response(status_code=401, content="Unauthorized access.")

    result = topic_service.unlock(id)
    if result is False:
        return Response(status_code=404, content="Topic not found.")
    return Response(status_code=200, content="Topic unlocked.")







