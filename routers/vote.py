from fastapi import APIRouter, Header
from data.models import Vote
from services import vote_service
from common.auth import verify_authenticated_user

vote_router = APIRouter(prefix='/votes')


@vote_router.get('/')
def get_votes(token: str = Header()):
    verify_authenticated_user(token)
    return vote_service.get_all()


@vote_router.put('/')
def vote(vote: Vote, token: str = Header()):
    verify_authenticated_user(token)
    return vote_service.vote(vote)