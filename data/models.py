
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    username: str
    is_admin: Optional[bool] = None
    email: str
    password: str

    @classmethod
    def from_query_result(cls,id,first_name,last_name,username,is_admin,email,password):
        return cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_admin=is_admin,
            email=email,
            password=password
        )



class Category(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None







class Topic(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: datetime





class Reply(BaseModel):
    id: Optional[int] = None
    content: str
    topics_id: int
    created_at: Optional[datetime] = None





class Conversation(BaseModel):
    id: Optional[int] = None
    users_id1: int
    users_id2: int
    created_at: Optional[datetime] = None




class Message(BaseModel):
    id: Optional[int] = None
    text: str
    conversation_id: int
    users_id: int
    sent_at: Optional[datetime] = None




class Vote(BaseModel):
    users_id: int
    reply_id: int
    type_vote: Optional[int] = None
    created_at: Optional[datetime] = None

