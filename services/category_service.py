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
        '''SELECT id, name, description
            FROM categories 
            WHERE id = ?''', (id,))

    return next((Category.from_query_result(*row) for row in data), None)

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


def create(category: Category):
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