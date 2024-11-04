from unicodedata import category
from data.database import insert_query, read_query, update_query
from data.models import Category
from services.user_service import is_admin

def get_all_public():
    data = read_query("select id, name, description, private,locked from categories where private = 0")
    return [Category.from_query_result(id, name, description, private,locked) for id, name, description, private,locked in data]

def get_all(user_id: int, token: str):
    if is_admin(token):
        data = read_query('SELECT id, name, description, private, locked FROM categories')
        return [Category.from_query_result(id, name, description, private,locked) for id, name, description, private,locked in data]

    else:
    
        data = read_query('''
            SELECT c.id, c.name, c.description, c.private,c.locked
            FROM categories c
            LEFT JOIN category_members cm ON c.id = cm.categories_id AND cm.users_id = ?
            WHERE c.private = 0 OR cm.users_id IS NOT NULL;
        ''', (user_id,))
        
        return [Category.from_query_result(id, name, description, private,locked) for id, name, description, private,locked in data]


def get_by_id(id: int, user_id: int, token: str):
    if is_admin(token):
        data = read_query('''SELECT c.id, c.name, c.description, c.private, t.name
            FROM categories c
            LEFT JOIN topics t ON c.id = t.categories_id
            WHERE c.id = ?''', (id,))
        is_admin_user = True
    else:
        data = read_query('''
            SELECT c.id, c.name, c.description, c.private, t.name,
                (SELECT COUNT(*) 
                    FROM category_members cm 
                    WHERE cm.categories_id = c.id AND cm.users_id = ?) AS is_member
            FROM categories c
            LEFT JOIN topics t ON c.id = t.categories_id
            WHERE c.id = ?
        ''', (user_id, id))
        is_admin_user = False

    category_with_topics = {}

    for row in data:
        cat_id = row[0]
        is_private = row[3]
        
        if not is_admin_user:
            is_member = row[5] 

            
            if is_private == 1 and is_member == 0:
                return None  

        if cat_id not in category_with_topics:
            category_with_topics[cat_id] = {
                "category_id": row[0],
                "category_name": row[1],
                "description": row[2],
                "topics": [],
                "private": is_private  
            }

        if row[4] is not None:  
            category_with_topics[cat_id]["topics"].append(row[4])

    return list(category_with_topics.values())



def get_by_name(name: str):
    data = read_query(
        '''SELECT id, name, description,private
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

def make_category_private(category_id: int):

    result = update_query('UPDATE categories SET private = 1 WHERE id = ?', (category_id,))


    user_ids = read_query('''
        SELECT DISTINCT t.author_id 
        FROM topics t 
        WHERE t.categories_id = ?
        UNION
        SELECT DISTINCT r.users_id
        FROM reply r
        JOIN topics t ON r.topics_id = t.id
        WHERE t.categories_id = ?
    ''', (category_id, category_id))


    for (user_id,) in user_ids:
        insert_query('''
                INSERT IGNORE INTO category_members (users_id, categories_id, access_type)
                VALUES (?, ?, 2)
            ''', (user_id, category_id))
    return result

# def update_access(category_id: int, private: int):
#     if not exists(category_id):
#         return False
#
#     return update_query(
#         'UPDATE categories SET private = ? WHERE id = ?',
#         (private, category_id)
#     )
def lock(id:int):
    data = read_query('''
        SELECT id, name, description, private,locked
        FROM categories
        WHERE id = ?
        ''', (id,))
    if data:
        return update_query(
        'UPDATE categories SET locked = 1 WHERE id = ?',
        (id,)
    )
    else:
        return False

def unlock(id:int):
    data = read_query('''
        SELECT id, name, description, private,locked
        FROM categories
        WHERE id = ?
        ''', (id,))
    if data:
        return update_query(
        'UPDATE categories SET locked = 0 WHERE id = ?',
        (id,)
    )
    else:
        return False

def check_private(id:int):
    data = read_query("""select private from categories where id = ?""", (id,))
    if data[0][0] == 1:
        return True
    else:
        return False