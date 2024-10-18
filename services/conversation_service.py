from data.database import insert_query, read_query
from data.models import Conversation


def get_all():
    data = read_query('select id, users_id1, users_id2, created_at from conversation')
    return [Conversation.from_query_result(*row) for row in data]

def get_by_id(id: int):
    data = read_query(
        '''SELECT id, users_id1, users_id2, created_at
            FROM conversation 
            WHERE id = ?''', (id,))

    return next((Conversation.from_query_result(*row) for row in data), None)
