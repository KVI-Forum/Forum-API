from data.models import Vote
from data.database import insert_query,read_query, update_query
from fastapi import Response ,Header
from common.auth import verify_authenticated_user



def vote(vote: Vote,token: str = Header()):
   verify_authenticated_user(token)
   user_id = int(token.split(';')[0])
   reply_id = vote.reply_id
   
   user_votes = get_all_user_replies(user_id)

   for user_vote in user_votes:
       if user_vote == reply_id:
            update_query('''update votes set type_vote = ? where users_id = ? and reply_id = ?''', (vote.type_vote,user_id,reply_id))
            return Response(status_code=200)

   insert_query('INSERT INTO votes (users_id, reply_id, type_vote) VALUES (?, ?, ?)', (user_id, reply_id, vote.type_vote))
   return Response(status_code=200)



def get_all_user_replies(user_id: int):
    result = read_query('''select reply_id from votes where users_id = ?''', (user_id,))

    return result


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



    