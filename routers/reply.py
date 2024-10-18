from fastapi import APIRouter, Response, Header

from common.auth import get_user_or_raise_401, verify_authenticated_user
from data.models import Reply
from services import reply_service

reply_router = APIRouter(prefix='/reply')

@reply_router.get('/')
def get_replies(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = reply_service.get_all(search)
    if result is None:
        return Response(status_code=404, content="No replies found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return reply_service.sort_replies(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result

@reply_router.post("/")
def create_reply(reply: Reply,token:str= Header()):

    verify_authenticated_user(token)
    reply_id = reply_service.create(reply.content,reply.topics_id, reply.users_id)
    if reply_id:
        return Response(status_code=200,content=f"reply with id:{reply_id} and content:'{reply.content}' was created at {reply.created_at}.")
    else:
        return Response(status_code=404, content="Topic or user not found.")