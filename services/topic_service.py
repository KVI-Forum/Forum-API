from data.models import Topic
from data.database import insert_query, read_query




def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, name, created_at from topics where name like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, name , created_at from topics ')
    
    return (Topic.from_query_result(id, name, created_at) for id, name, created_at in data)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, name, created_at
            FROM topics 
            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


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

def sort_categories(topics: list[Topic], *, attribute='name', reverse=False):
    if attribute == 'name':
        def sort_fn(t: Topic): return t.name
    elif attribute == 'created_at':
        def sort_fn(t: Topic): return t.created_at
    else:
        def sort_fn(t: Topic): return t.id
    
    return sorted(topics, key=sort_fn, reverse=reverse)