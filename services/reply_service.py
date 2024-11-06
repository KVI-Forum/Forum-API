from datetime import datetime

from fastapi import Response
from data.models import Reply
from data.database import insert_query, read_query
from services import topic_service, user_service


def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, content,topics_id,users_id, created_at from reply where id like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, content, topics_id, users_id, created_at from reply ')

    return (Reply.from_query_result(id, content,topics_id,users_id, created_at) for id,content, topics_id,users_id, created_at in data)


def sort_replies(replies: list[Reply], *, attribute='created_at', reverse=False):

    if attribute == 'created_at':
        def sort_fn(r: Reply):
            return r.created_at
    else:
        def sort_fn(r: Reply):
            return r.id

    return sorted(replies, key=sort_fn, reverse=reverse)

def create(content:str,topics_id:int,users_id:int):

    topic = topic_service.get_by_id(topics_id,users_id)
    user = user_service.get_user_by_id(users_id)

    if not topic:
        return None
    create_datetime = datetime.now()
    generated_id = insert_query("""insert into reply(content,topics_id,users_id,created_at)
    VALUES(?,?,?,?)""",(content,topics_id,users_id,create_datetime))
    return generated_id,create_datetime

def get_by_topic_id(topic_id: int):
    data = read_query('select id, content, topics_id, users_id, created_at from reply where topics_id = ?',
                      (topic_id,))
    return (Reply.from_query_result(id, content, topics_id, users_id, created_at) for id, content, topics_id, users_id, created_at in data)

def get_upvotes(reply_id: int):
    data = read_query('select count(*) from votes where reply_id = ? and type_vote = 1', (reply_id,))
    return int(data[0][0])

def get_downvotes(reply_id: int):
    data = read_query('select count(*) from votes where reply_id = ? and type_vote = 0', (reply_id,))
    return int(data[0][0])

def get_reply_author_name(reply_id: int):
    data = read_query('select username from users where id = (select users_id from reply where id = ?)', (reply_id,))
    return data[0][0]
