from data.models import Vote
from data.database import insert_query,read_query, update_query
from fastapi import Response ,Header
from common.auth import verify_authenticated_user



def vote(vote: Vote, user_id: int):
    reply_id = vote.reply_id


    user_vote = read_query(
        '''SELECT reply_id FROM votes WHERE users_id = ? AND reply_id = ?''',
        (user_id, reply_id)
    )

    if user_vote:
        update_query(
            '''UPDATE votes SET type_vote = ? WHERE users_id = ? AND reply_id = ?''',
            (vote.type_vote, user_id, reply_id)
        )
        return Response(status_code=200, content="Vote updated")
    else:
        insert_query(
            '''INSERT INTO votes (users_id, reply_id, type_vote) VALUES (?, ?, ?)''',
            (user_id, reply_id, vote.type_vote)
        )
        return Response(status_code=201, content="New vote created")


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



    