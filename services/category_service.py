from unicodedata import category

from data.database import insert_query, read_query, update_query
from data.models import Category


def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, name, description,locked from categories where name like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, name , description,locked from categories ')
    
    return (Category.from_query_result(id, name, description,locked) for id, name, description,locked in data)


def get_by_id(id: int):
    data = read_query('''
        SELECT c.id, c.name, c.description, c.locked, t.name
        FROM categories c
        LEFT JOIN topics t ON c.id = t.categories_id
        WHERE c.id = ?
    ''', (id,))

    category_with_topics = {}

    for row in data:
        cat_id = row[0]

        if cat_id not in category_with_topics:
            category_with_topics[cat_id] = {
                "category_id": row[0],
                "category_name": row[1],
                "description": row[2],
                "topics": [],
                "locked": row[3]  # Ensure 'locked' is correctly stored here
            }

        if row[4] is not None:  # row[4] now refers to 't.name' for topics
            category_with_topics[cat_id]["topics"].append(row[4])

    return list(category_with_topics.values())


def get_by_name(name: str):
    data = read_query(
        '''SELECT id, name, description
            FROM categories 
            WHERE name = ?''', (name,))

    return next((Category.from_query_result(*row) for row in data), None)

def exists(id: int):
    return any(
        read_query(
            'select id, name from categories where id = ?',
            (id,)))


def create(category_name:str, description:str, ):
    category_check= get_by_name(category_name)
    if category_check:
        return None

    generated_id = insert_query(
        'insert into categories(name,description) values(?,?)',
        (category_name,description))

    return generated_id

def sort_categories(categories: list[Category], *, attribute='name', reverse=False):
    if attribute == 'name':
        def sort_fn(c: Category): return c.name
    elif attribute == 'description':
        def sort_fn(c: Category): return c.description
    else:
        def sort_fn(c: Category): return c.id
    
    return sorted(categories, key=sort_fn, reverse=reverse)


def update_access(category_id: int, locked: int):
    if not exists(category_id):
        return False
    
    return update_query(
        'UPDATE categories SET locked = ? WHERE id = ?',
        (locked, category_id)
    )
