from data.models import Vote
from data.database import insert_query,read_query, update_query
from fastapi import Response ,Header
from common.auth import verify_authenticated_user



def vote(vote: Vote,token: str = Header()):
   verify_authenticated_user(token)
   user_id = token[0]
   reply_id = get_all_user_replies(user_id)[1]
   


def get_all_user_replies(user_id: int):
    result = read_query('''select * from votes where users_id = ?''', (user_id,))

    votes = [
        {
            'users_id': row[0],
            'reply_id': row[1],
            'type_vote': row[2],
            'created_at': row[3].strftime('%Y-%m-%d %H:%M:%S')
        } for row in result
    ]

    return votes


def get_all():
    result = read_query('''select * from votes''')

    votes = [
        {
            'users_id': row[0],
            'reply_id': row[1],
            'type_vote': row[2],
            'created_at': row[3].strftime('%Y-%m-%d %H:%M:%S')
        } for row in result
    ]

    return votes



    