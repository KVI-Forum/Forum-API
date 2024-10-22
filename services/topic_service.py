from fastapi import Response
from data.models import Topic
from data.database import insert_query, read_query, update_query
from services import category_service


def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, name, created_at,categories_id,author_id from topics where name like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, name , created_at, categories_id,author_id from topics ')
    
    return (Topic.from_query_result(id, name, created_at,categories_id,author_id) for id, name, created_at,categories_id,author_id in data)


def get_by_id(id: int):
    data = read_query(
        '''
        SELECT t.id, t.name, t.created_at, t.categories_id,author_id, r.content
        FROM topics t
        LEFT JOIN reply r ON t.id = r.topics_id
        WHERE t.id = ?
        ''', (id,)
    )

    topic_with_replies = {}

    for row in data:
        topic_id = row[0]

        if topic_id not in topic_with_replies:

            topic_with_replies[topic_id] = {
                "topic_id": row[0],
                "topic_name": row[1],
                "created_at": row[2],
                "categories_id": row[3],
                "author_id": row[4],
                "reply_content": []
            }

        if row[5] is not None:
            topic_with_replies[topic_id]["reply_content"].append(row[5])
    return list(topic_with_replies.values())


# def exists(id: int):
#     return any(
#         read_query(
#             'select id, name from categories where id = ?',
#             (id,)))


# def create(category: Category):
#     generated_id = insert_query(
#         'insert into categories(name) values(?)',
#         (category.name,))

#     category.id = generated_id

#     return category

def sort_topics(topics: list[Topic], *, attribute='name', reverse=False):
    if attribute == 'name':
        def sort_fn(t: Topic): return t.name
    elif attribute == 'created_at':
        def sort_fn(t: Topic): return t.created_at
    else:
        def sort_fn(t: Topic): return t.id
    
    return sorted(topics, key=sort_fn, reverse=reverse)

def create(topic_name:str,cat_id:int,author_id:int):
    category = category_service.get_by_id(cat_id)
    if not category:
        return None

    generated_id = insert_query("""insert into topics(name,categories_id,author_id)
    VALUES(?,?,?)""",(topic_name,cat_id,author_id))
    return generated_id


def update_best_reply(topic_id: int, reply_id: int, user_id: int):
    topic = get_by_id(topic_id)
    if not topic:
        return None

    author_id = topic[0]['author_id']
    if int(author_id) != int(user_id):
        return False

    print(f"Updating topic {topic_id} with best reply {reply_id}")
    update_result = update_query('UPDATE topics SET best_reply_id = ? WHERE id = ?', (reply_id, topic_id))
    print(f"Update result: {update_result}")

    # topic = get_by_id(topic_id)
    # if not topic:
    #     return None
    
    # if topic[0]['author_id'] != user_id:
    #     return False
    
    # update_result = update_query('UPDATE topics SET best_reply_id = ? WHERE id = ?', (reply_id, topic_id))
    # return update_result
    




    


