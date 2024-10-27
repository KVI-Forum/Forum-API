from data.models import Vote
from data.database import insert_query,read_query, update_query
from fastapi import Response ,Header
from common.auth import verify_authenticated_user


def upvote(id: int, user_id: int):
    user_vote = read_query(
        '''SELECT reply_id FROM votes WHERE users_id = ? AND reply_id = ?''',
        (user_id, id)
    )

    if user_vote:
        update_query(
            '''UPDATE votes SET type_vote = 1 WHERE users_id = ? AND reply_id = ?''',
            ( user_id, id)
        )
        return Response(status_code=200, content="Upvoted!")
    else:
        insert_query(
            '''INSERT INTO votes (users_id, reply_id, type_vote) VALUES (?, ?, 1)''',
            (user_id, id)
        )
        return Response(status_code=201, content="Upvoted!")

def downvote(id: int, user_id: int):
    user_vote = read_query(
        '''SELECT reply_id FROM votes WHERE users_id = ? AND reply_id = ?''',
        (user_id, id)
    )

    if user_vote:
        update_query(
            '''UPDATE votes SET type_vote = 0 WHERE users_id = ? AND reply_id = ?''',
            (user_id, id)
        )
        return Response(status_code=200, content="Downvoted!")
    else:
        insert_query(
            '''INSERT INTO votes (users_id, reply_id, type_vote) VALUES (?, ?, 0)''',
            (user_id, id)
        )
        return Response(status_code=201, content="Upvoted!")




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



    