from data.database import insert_query, read_query
from data.models import Conversation


def get_all(user_id):
    data = read_query('select id, users_id1, users_id2, created_at from conversation where users_id1 = ? or users_id2 = ?', (user_id,user_id))
    return [Conversation.from_query_result(*row) for row in data]


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

    # Dictionary to store the conversation and its messages with sender name
    conversation_with_messages = None

    for row in data:
        # Initialize the conversation if not already done
        if conversation_with_messages is None:
            conversation_with_messages = {
                "conversation_id": row[0],
                "users_id1": row[1],
                "users_id2": row[2],
                "created_at": row[3],
                "messages": []
            }

        # Append messages along with the sender's name if message exists
        if row[4] is not None:
            conversation_with_messages["messages"].append({
                "text": row[4],
                "sender_name": row[5]  # Sender's name
            })

    return conversation_with_messages
