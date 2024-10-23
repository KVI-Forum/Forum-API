from http.client import HTTPException

from starlette.responses import Response

from data.database import insert_query, read_query
from data.models import User

_SEPARATOR = ';'

def all_users():
    data = read_query('SELECT id, first_name, last_name, username, email, is_admin FROM users ORDER BY id')
    return (User(id=id, first_name=first_name, last_name=last_name, username=username, email=email, is_admin=is_admin)
            for id, first_name, last_name, username, email, is_admin in data)


def get_user_by_id(user_id: int):
    data = read_query('SELECT id, first_name, last_name, username, email, is_admin FROM users WHERE id = ?',
                      (user_id,))
    return next((User(id=id, first_name=first_name, last_name=last_name, username=username, email=email, is_admin=is_admin)
                 for id, first_name, last_name, username, email, is_admin in data), None)

def user_exists(user_id: int):
    return any(read_query('SELECT id FROM users WHERE id = ?', (user_id,)))


def create_user(user: User):
    duplicate = read_query("""select username from users where username = ?""", (user.username,))
    if duplicate:
        return None
    duplicate = read_query("""select email from users where email = ?""", (user.email,))
    if duplicate:
        return None

    generated_id = insert_query(
        'INSERT INTO users (first_name, last_name, username, password, email) VALUES (?, ?, ?, ?, ?)',
        (user.first_name, user.last_name, user.username, user.password, user.email)
    )
    user.id = generated_id
    return user


def create_token(user: User):
    return f'{user.id};{user.username}'


def try_login(username: str, password: str):
    data = read_query('SELECT id, first_name, last_name, username, email, password, is_admin FROM users WHERE username = ? AND password = ?',
                      (username, password))
    
    return next((User(id=id, first_name=firstname, last_name=lastname, username=username, email=email, password=password, is_admin=is_admin)
                 for id, firstname, lastname, username, email, password, is_admin in data), None)

def is_authenticated(token: str) -> bool: # TODO FIX 
    return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        token.split(_SEPARATOR)))


def is_admin(token: str):

    user_id, username = token.split(_SEPARATOR)
    data = read_query('''SELECT is_admin FROM users WHERE id = ? AND username = ?''', [user_id, username])
    if data and data[0][0] == 1:
        return True
    return False

def find_by_username(username: str):
    data = read_query('SELECT id, first_name, last_name, username, email, password, is_admin FROM users WHERE username = ?',
                      (username,))
    return next((User(id=id, first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=is_admin)
                 for id, first_name, last_name, username, email, password, is_admin in data), None)



def from_token(token: str) -> User | None:
    _, username = token.split(_SEPARATOR)

    return find_by_username(username)