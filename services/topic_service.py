from fastapi import Response
from data.models import Topic
from data.database import insert_query, read_query, update_query
from services import category_service


def get_all(user_id: int, search: str = None):
    query = '''
        SELECT t.id, t.name, t.created_at, t.categories_id, t.author_id, t.locked
        FROM topics t
        JOIN categories c ON t.categories_id = c.id
        LEFT JOIN category_members cm ON t.categories_id = cm.categories_id AND cm.users_id = ?
        WHERE (c.private = 0 OR t.author_id = ? OR cm.users_id IS NOT NULL) 
    '''
    params = [user_id, user_id]

    if search:
        query += " AND t.name LIKE ?"
        params.append(f'%{search}%')
    data = read_query(query, params)

    return [Topic.from_query_result(id, name, created_at, categories_id, author_id, locked)
            for id, name, created_at, categories_id, author_id, locked in data]

def exists(id:int):
    data = read_query("""select  id, name, created_at, categories_id, author_id, locked
     from topics where id= ?""",(id,) )
    return data

def get_by_id(id: int, user_id: int):
    data = read_query(
        '''
        SELECT t.id, t.name, t.created_at, t.categories_id, t.author_id, t.locked, r.content
        FROM topics t
        LEFT JOIN reply r ON t.id = r.topics_id
        LEFT JOIN category_members cm ON cm.categories_id = t.categories_id
        WHERE t.id = ? AND (t.categories_id NOT IN (SELECT id FROM categories WHERE private = 1)
                            OR cm.users_id = ? OR t.author_id = ?)
        ''', (id, user_id, user_id)
    )

    if not data:
        return None
    return construct_response(data)

def construct_response(data):
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
                "locked": row[5],
                "reply_content": []
            }

        if row[6] is not None:
            topic_with_replies[topic_id]["reply_content"].append(row[6])
    return list(topic_with_replies.values())

def sort_topics(topics: list[Topic], *, attribute='name', reverse=False):
    if attribute == 'name':
        def sort_fn(t: Topic): return t.name
    elif attribute == 'created_at':
        def sort_fn(t: Topic): return t.created_at
    else:
        def sort_fn(t: Topic): return t.id
    
    return sorted(topics, key=sort_fn, reverse=reverse)

def create(topic_name:str,cat_id:int,author_id:int,token:str,):
    category = category_service.get_by_id(cat_id,author_id,token)
    if not category:
        return None
    cat_info = read_query("select locked,private from categories where id = ?",(cat_id,))
    if cat_info[0][0] == 1:
        return False
    if cat_info[0][1] == 1:
        access_data = read_query(
            """
            SELECT access_type FROM category_members
            WHERE categories_id = ? AND users_id = ?
            """,
            (cat_id, author_id)
        )

        if not access_data or access_data[0][0] < 2:
            return False

    generated_id = insert_query("""insert into topics(name,categories_id,author_id)
    VALUES(?,?,?)""",(topic_name,cat_id,author_id))
    return generated_id


def update_best_reply(topic_id: int, reply_id: int, user_id: int):
    topic = get_by_id(topic_id,user_id)
    if not topic:
        return None

    author_id = topic[0]['author_id']
    if int(author_id) != int(user_id):
        return False

    print(f"Updating topic {topic_id} with best reply {reply_id}")
    update_result = update_query('UPDATE topics SET best_reply_id = ? WHERE id = ?', (reply_id, topic_id))
    print(f"Update result: {update_result}")

def lock(id:int):
    data = read_query('''
        SELECT id, name, created_at, categories_id,author_id, locked
        FROM topics
        WHERE id = ?
        ''', (id,))
    if data:
        return update_query(
        'UPDATE topics SET locked = 1 WHERE id = ?',
        (id,)
    )
    else:
        return False

def unlock(id:int):
    data = read_query('''
        SELECT id, name, created_at, categories_id,author_id, locked
        FROM topics
        WHERE id = ?
        ''', (id,))
    if data:
        return update_query(
        'UPDATE topics SET locked = 0 WHERE id = ?',
        (id,)
    )
    else:
        return False




    


