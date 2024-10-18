
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional
# TODO: add field validation
# TODO: fix the user model and service
class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    username: str
    is_admin: Optional[bool] = False
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
    
class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str



class Category(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

    @classmethod
    def from_query_result(cls,id,name,description):
        return cls(
            id=id,
            name=name,
            description=description
        )







class Topic(BaseModel):
    id: Optional[int] = None
    name: str
    created_at: Optional[datetime] = None
    categories_id: int

    @classmethod
    def from_query_result(cls,id,name,created_at,categories_id):
        return cls(
            id=id,
            name=name,
            created_at=created_at,
            categories_id=categories_id

        )



class Reply(BaseModel):
    id: Optional[int] = None
    content: str
    topics_id: int
    users_id:int
    created_at: Optional[datetime] = None
    @classmethod
    def from_query_result(cls,id,content,topics_id,users_id,created_at):
        return cls(
            id=id,
            content=content,
            topics_id=topics_id,
            users_id= users_id,
            created_at=created_at
        )




class Conversation(BaseModel):
    id: Optional[int] = None
    users_id1: int
    users_id2: int
    created_at: Optional[datetime] = None

    @classmethod
    def from_query_result(cls,id,users_id1,users_id2,created_at):
        return cls(
            id=id,
            users_id1=users_id1,
            users_id2=users_id2,
            created_at=created_at
        )




class Message(BaseModel):
    id: Optional[int] = None
    text: str
    conversation_id: int
    users_id: int
    sent_at: Optional[datetime] = None

    @classmethod
    def from_query_result(cls,id,text,conversation_id,users_id,sent_at):
        return cls(
            id=id,
            text=text,
            conversation_id=conversation_id,
            users_id=users_id,
            sent_at=sent_at
        )




class Vote(BaseModel):
    users_id: int
    reply_id: int
    type_vote: Optional[int] = None
    created_at: Optional[datetime] = None


TUsername = constr(pattern=r'^[a-zA-Z0-9_]{3,}$')
TPassword = constr(min_length=5, max_length=32)


class LoginData(BaseModel):
    username: TUsername #type: ignore
    password: TPassword #type: ignore
