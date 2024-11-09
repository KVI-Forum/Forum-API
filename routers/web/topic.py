from fastapi import APIRouter, Request, Form, Response
from common.template_config import CustomJinja2Templates
from services import topic_service,user_service,reply_service,vote_service
from fastapi.responses import RedirectResponse
from common.auth import verify_authenticated_user
topic_router = APIRouter(prefix='/topics')
templates = CustomJinja2Templates(directory='templates')

@topic_router.get('/{topic_id}')
def get_topic_by_id(request: Request, topic_id: int):
    token = request.cookies.get('token')
    if not token:
        return RedirectResponse(url='/users/login',status_code=302)
    user_id = int(token.split(';')[0])
    topic = topic_service.get_by_id(topic_id, user_id)
    if not topic:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Topic not found"})
    
    replies = reply_service.get_by_topic_id(topic_id)
    topic_author = user_service.get_user_by_id(topic["author_id"])
    access = user_service.get_user_access(user_id)

    topic_author = topic_author.username

    return templates.TemplateResponse("topic.html", {"request": request, "topic": topic, "replies": replies, "access": access,  "topic_author": topic_author, "topic_id": topic_id })


@topic_router.post("/{topic_id}/replies")
def post_reply(
    topic_id: int,
    request: Request,
    content: str = Form(...),
    token: str = Form(...)
):
   
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)

    reply_id = reply_service.create(content, topic_id, user_id)
    
    if reply_id:
        return RedirectResponse(f'/topics/{topic_id}',status_code=302)
        
    else:
        return templates.TemplateResponse("fail.html", {"request": request})

@topic_router.post('/{topic_id}/upvote/{reply_id}')
def vote(topic_id:int, reply_id : int, token: str = Form(...)):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    vote = vote_service.upvote(reply_id,user_id)
    if vote :
        return RedirectResponse(f'/topics/{topic_id}',status_code=302)
    else:
        return Response(status_code=404,content="Access is restricted.")

@topic_router.post('/{topic_id}/downvote/{reply_id}')
def vote(topic_id:int,reply_id : int, token: str = Form(...)):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    vote = vote_service.downvote(reply_id,user_id)
    if vote :
        return RedirectResponse(f'/topics/{topic_id}',status_code=302)
    else:
        return Response(status_code=404,content="Access is restricted.")

@topic_router.post('/{topic_id}/replies/{reply_id}/best_reply')
def best_reply(topic_id:int,reply_id : int, token: str = Form(...)):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
   
    reply = topic_service.update_best_reply(topic_id,reply_id,user_id)
    if reply:
        return RedirectResponse(f'/topics/{topic_id}',status_code=302)
        
    else:
        return Response(status_code=404,content="Access is restricted.")