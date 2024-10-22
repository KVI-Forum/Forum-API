from data.database import insert_query, read_query
from data.models import Category


def get_all(search: str = None):
    if search:
        data = read_query(
            'select id, name, description from categories where name like ? ',
            (f'%{search}%',))
    else:
        data = read_query('select id, name , description from categories ')
    
    return (Category.from_query_result(id, name, description) for id, name, description in data)


def get_by_id(id: int):
    data = read_query(
        '''
        SELECT c.id, c.name, c.description, t.name
        FROM categories c
        LEFT JOIN topics t ON c.id = t.categories_id
        WHERE c.id = ?
        ''', (id,)
    )

    category_with_topics = {}

    for row in data:
        cat_id = row[0]

        if cat_id not in category_with_topics:

            category_with_topics[cat_id] = {
                "category_id": row[0],
                "category_name": row[1],
                "description": row[2],
                "topics":[]

            }

        if row[3] is not None:
            category_with_topics[cat_id]["topics"].append(row[3])
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


def create_category(category: Category):
    generated_id = insert_query(
        'insert into categories(name) values(?)',
        (category.name,))

    category.id = generated_id

    return category

def sort_categories(categories: list[Category], *, attribute='name', reverse=False):
    if attribute == 'name':
        def sort_fn(c: Category): return c.name
    elif attribute == 'description':
        def sort_fn(c: Category): return c.description
    else:
        def sort_fn(c: Category): return c.id
    
    return sorted(categories, key=sort_fn, reverse=reverse)