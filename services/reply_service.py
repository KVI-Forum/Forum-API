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
    topic = topic_service.get_by_id(topics_id)
    # user = user_service.get_user_by_id(users_id)

    if not topic:
        return None

    generated_id = insert_query("""insert into reply(content,topics_id,users_id)
    VALUES(?,?,?)""",(content,topic.id,users_id))
    return generated_id