from fastapi import APIRouter, Response, Header
from data.models import Message 
from services import message_service 
from common.auth import verify_authenticated_user

message_router = APIRouter(prefix='/api/messages')

@message_router.get('')
def get_messages(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = message_service.get_all(search)
    if result is None:
        return Response(status_code=404, content="No messages found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return message_service.sort_messages(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result
        
@message_router.get('/{id}')
def get_message_by_id(id: int):
    result = message_service.get_by_id(id)
    if result is None:
        return Response(status_code=404, content="Message not found.")
    else:
        return result
    
@message_router.post('')
def create_message(message: Message,token:str = Header()):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    message_id, date_time_stamp = message_service.create(message.text, message.conversation_id, user_id)

    if message_id:
        formatted_created_at = date_time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        return Response(status_code=200, content=f"Message with id: {message_id} and text: '{message.text}' was sent at {formatted_created_at} ")
    else:
        return Response(status_code=404, content="Conversation or user not found.")

    