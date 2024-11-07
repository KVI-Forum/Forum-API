from fastapi import APIRouter, Request, Form
from common.template_config import CustomJinja2Templates
from services import topic_service,user_service,reply_service
from fastapi.responses import RedirectResponse
from common.auth import verify_authenticated_user
topic_router = APIRouter(prefix='/topic')
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
    upvotes = reply_service.get_upvotes(topic_id)
    downvotes = reply_service.get_downvotes(topic_id)

    topic_author = topic_author.username

    return templates.TemplateResponse("topic.html", {"request": request, "topic": topic, "replies": replies, "access": access, "upvotes": upvotes, "downvotes": downvotes, "topic_author": topic_author, "topic_id": topic_id })


@topic_router.post("/{topic_id}/reply")
def post_reply(
    topic_id: int,
    request: Request,
    content: str = Form(...),
    token: str = Form(...)
):
    # Extract user_id from token
    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    
    # Call your reply service to create a reply
    reply_id = reply_service.create(content, topic_id, user_id)
    
    if reply_id:
        # formatted_created_at = create_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return RedirectResponse(f'/topic/{topic_id}',status_code=302)
        
    else:
        return templates.TemplateResponse("fail.html", {"request": request})
