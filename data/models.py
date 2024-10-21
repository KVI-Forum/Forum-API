
# type: ignore

from pydantic import Field, BaseModel, constr
from datetime import datetime
from typing import Optional

# TODO: fix the user service

class User(BaseModel):
    id: Optional[int] = None
    first_name: constr(min_length=2, max_length=30) = Field(..., description="First name of the user")   
    last_name: constr(min_length=2, max_length=30) = Field(..., description="Last name of the user")   
    username: constr(min_length=4, max_length=20) = Field(..., description="Username with minimum 4 and maximum 20 characters") 
    is_admin: Optional[bool] = Field(False, description="Whether the user has admin privileges") 
    password: constr(min_length=8) = Field(..., description="Password must have at least 8 characters") 
    email: constr(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$') = Field(..., description="Email address of the user")

    @classmethod
    def from_query_result(cls,id,first_name,last_name,username,is_admin,password, email):
        return cls(
            id=id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            is_admin=is_admin,
            password=password,
            email=email,
        )
    

  # password -> <- email ?  
class UserRegistration(BaseModel):
    first_name: constr(min_length=2, max_length=30) = Field(..., description="First name of the user")
    last_name: constr(min_length=2, max_length=30) = Field(..., description="Last name of the user")
    username: constr(min_length=4, max_length=20) = Field(..., description="Username with minimum 4 and maximum 20 characters")
    password: constr(min_length=8) = Field(..., description="Password must have at least 8 characters")
    email: constr(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$') = Field(..., description="Email address of the user")



class Category(BaseModel):
    id: Optional[int] = None
    name: constr(min_length=3, max_length=50) = Field(..., description='Name for the category')
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
    name: constr(min_length=1, max_length=100) = Field(..., description='Name of the topic')
    created_at: Optional[datetime] = None
    categories_id: int = Field(..., description="ID of the category associated with the topic")

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
    content: constr(min_length=1, max_length=500) = Field(..., description='Content of the reply')
    topics_id: int = Field(..., description='ID of topic associated with the reply')
    users_id:int = Field(..., description='ID of the user which created the reply')
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
    users_id1: int = Field(..., description='User ID associated with the conversation')
    users_id2: int = Field(..., description='User ID associated with the conversation')
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
    text: constr(min_length=2, max_length=500) = Field(..., description='Text of the message')
    conversation_id: int = Field(..., description= 'ID associated with the conversation of the message')
    users_id: int = Field(..., description= 'ID associated with the user creating the message')
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
    users_id: int = Field(...,description= 'ID associated with the user voting')
    reply_id: int = Field(...,description= 'ID associated with reply of the vote')
    type_vote: Optional[int] = None
    created_at: Optional[datetime] = None


TUsername = constr(pattern=r'^[a-zA-Z0-9_]{3,}$')
TPassword = constr(min_length=5, max_length=32)


class LoginData(BaseModel):
    username: TUsername #type: ignore
    password: TPassword #type: ignore

