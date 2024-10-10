from data.database import insert_query, read_query
from data.models import User


def all_users():
    data = read_query('SELECT idusers, firstname, lastname, username, email, is_admin FROM users ORDER BY idusers')
    return (User(idusers=idusers, firstname=firstname, lastname=lastname, username=username, email=email, is_admin=is_admin) for idusers, firstname, lastname, username, email, is_admin in data)

def get_user_by_id(user_id: int):
    data = read_query('SELECT idusers, firstname, lastname, username, email, is_admin FROM users WHERE idusers = ?',
                      (user_id,))
    return next((User(idusers=idusers, firstname=firstname, lastname=lastname, username=username, email=email, is_admin=is_admin)
                 for idusers, firstname, lastname, username, email, is_admin in data), None)

def user_exists(user_id: int):
    return any(read_query('SELECT idusers FROM users WHERE idusers = ?', (user_id,)))

def create_user(user: User):
    generated_id = insert_query(
        'INSERT INTO users (firstname, lastname, username, password, email, is_admin) VALUES (?, ?, ?, ?, ?, ?)',
        (user.firstname, user.lastname, user.username, user.password, user.email, user.is_admin))

    user.idusers = generated_id
    return user