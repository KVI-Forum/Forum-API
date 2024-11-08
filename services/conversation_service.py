from data.database import insert_query, read_query
from data.models import Conversation


def get_all(user_id):
    data = read_query('select id, users_id1, users_id2, created_at from conversation where users_id1 = ? or users_id2 = ?', (user_id,user_id))
    return [Conversation.from_query_result(*row) for row in data]

def exists(id):
    data = read_query('''select id, users_id1, users_id2, created_at from conversation
     where id = ?''',(id,))
    return data
def get_by_id(id: int, user_id: int):
    data = read_query(
        '''
        SELECT c.id, c.users_id1, c.users_id2, c.created_at, m.text, u.first_name
        FROM conversation c
        LEFT JOIN messages m ON c.id = m.conversation_id
        LEFT JOIN users u ON m.users_id = u.id
        WHERE c.id = ? AND (c.users_id1 = ? OR c.users_id2 = ?)
        ''', (id, user_id, user_id)
    )


    conversation_with_messages = None

    for row in data:
        if conversation_with_messages is None:
            conversation_with_messages = {
                "conversation_id": row[0],
                "users_id1": row[1],
                "users_id2": row[2],
                "created_at": row[3],
                "messages": []
            }

        if row[4] is not None:
            conversation_with_messages["messages"].append({
                "text": row[4],
                "sender_name": row[5]
            })

    return conversation_with_messages

def get_by_user_ids(user_id1: int, user_id2: int):
    data = read_query(
        '''
        SELECT id, users_id1, users_id2, created_at
        FROM conversation
        WHERE (users_id1 = ? AND users_id2 = ?) OR (users_id1 = ? AND users_id2 = ?)
        ''', (user_id1, user_id2, user_id2, user_id1)
    )

    return Conversation.from_query_result(*data[0]) if data else None