from data.database import insert_query, read_query
from data.models import User


def all_users():
    data = read_query('SELECT id, firstname, lastname, username, email, is_admin FROM users ORDER BY id')
    return (User(id=id, first_name=firstname, last_name=lastname, username=username, email=email, is_admin=is_admin)
            for id, firstname, lastname, username, email, is_admin in data)


def get_user_by_id(user_id: int):
    data = read_query('SELECT id, firstname, lastname, username, email, is_admin FROM users WHERE id = ?',
                      (user_id,))
    return next((User(id=id, first_name=firstname, last_name=lastname, username=username, email=email, is_admin=is_admin)
                 for id, firstname, lastname, username, email, is_admin in data), None)

def user_exists(user_id: int):
    return any(read_query('SELECT id FROM users WHERE id = ?', (user_id,)))


def create_user(user: User):
    generated_id = insert_query(
        'INSERT INTO users (firstname, lastname, username, password, email) VALUES (?, ?, ?, ?, ?)',
        (user.firstname, user.lastname, user.username, user.password, user.email)
    )
    user.id = generated_id
    return user


def create_token(user: User):
    return f'{user.id};{user.username}'


def try_login(username: str, password: str):
    data = read_query('SELECT id, firstname, lastname, username, email, is_admin FROM users WHERE username = ? AND password = ?',
                      (username, password))
    
    return next((User(id=id, first_name=firstname, last_name=lastname, username=username, email=email, is_admin=is_admin)
                 for id, firstname, lastname, username, email, is_admin in data), None)
