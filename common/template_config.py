from fastapi.templating import Jinja2Templates
from common.auth import get_user_if_token
from services.reply_service import get_reply_author_name, get_upvotes, get_downvotes

class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = get_user_if_token
        self.env.globals['get_reply_author'] = get_reply_author_name
        self.env.globals['get_upvotes'] = get_upvotes
        self.env.globals['get_downvotes']  = get_downvotes
