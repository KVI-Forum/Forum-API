import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.api.category import category_router as api_category_router
from routers.api.reply import reply_router as api_reply_router
from routers.api.topic import topic_router as api_topic_router
from routers.api.user import users_router as api_users_router
from routers.api.message import message_router as api_message_router
from routers.api.conversation import conversation_router as api_conversation_router
from routers.web.home import index_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_category_router)
app.include_router(api_topic_router)
app.include_router(api_users_router)
app.include_router(api_reply_router)
app.include_router(api_message_router)
app.include_router(api_conversation_router)
app.include_router(index_router)







# TODO Topics in a private category are only available to category members

# TODO: Add an option to lock topics in the system.

# TODO: Refactor the following components to implement access-related changes:
#       - Topic reply
#       - Category services
#       - Routers
#       - Topic service
#       - Reply service
#       - User service

if __name__ == "__main__":
    uvicorn.run('main:app')


# todo remove all verbs