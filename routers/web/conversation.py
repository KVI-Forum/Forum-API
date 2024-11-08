from fastapi import APIRouter, Request, Form
from common.template_config import CustomJinja2Templates
from services import user_service, conversation_service, message_service
from fastapi.responses import RedirectResponse



conversation_router = APIRouter(prefix='/conversations')
templates = CustomJinja2Templates(directory='templates')

@conversation_router.get('/{user_id}')
def get_conversations(request: Request, user_id: int):
    sender_id = int(request.cookies.get('token').split(';')[0])
    user = user_service.get_user_by_id(user_id)
    conversation = conversation_service.get_by_user_ids(sender_id, user_id)
    messages = message_service.get_by_conversation_id(conversation.id)


    return templates.TemplateResponse("conversation.html", {"request": request, "user": user, "conversation": conversation, "messages": messages})


@conversation_router.post('/{user_id}/messages')
def post_message(
    user_id: int,
    request: Request,
    content: str = Form(...),
    token: str = Form(...)
):
    sender_id = int(token.split(";")[0])
    conversation = conversation_service.get_by_user_ids(sender_id, user_id)
    message = message_service.create(content, conversation.id, sender_id)

    if message:
        return RedirectResponse(f'/conversations/{user_id}',status_code=302)
    else:
        return templates.TemplateResponse("fail.html", {"request": request})