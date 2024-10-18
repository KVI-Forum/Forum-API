from fastapi import FastAPI
from routers.category import category_router
from routers.reply import reply_router
from routers.topic import topic_router
from routers.user import users_router

app = FastAPI()
app.include_router(category_router)
app.include_router(topic_router)
app.include_router(users_router)
app.include_router(reply_router)