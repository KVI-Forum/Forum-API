from datetime import datetime

from data.database import insert_query, read_query
from data.models import Message 


def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, text, conversation_id , users_id , sent_at from messages where content like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, text, conversation_id , users_id , sent_at from messages ')

    return [Message.from_query_result(*row) for row in data]

def sort_messages(messages: list[Message], *, attribute='sent_at', reverse=False):

    if attribute == 'sent_at':
        def sort_fn(m: Message):
            return m.sent_at
    else:
        def sort_fn(m: Message):
            return m.id

    return sorted(messages, key=sort_fn, reverse=reverse)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, text, conversation_id , users_id , sent_at
            FROM messages 
            WHERE id = ?''', (id,))

    return next((Message.from_query_result(*row) for row in data), None)

def create(text: str, conversation_id: int, users_id: int):
    sent_datetime = datetime.now()
    generated_id =  insert_query(
        '''INSERT INTO messages (text, conversation_id, users_id,sent_at)
            VALUES (?, ?, ?, ?)''',
        (text, conversation_id, users_id,sent_datetime))
    return generated_id, sent_datetime