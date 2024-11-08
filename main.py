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
from routers.web.users import users_router, access_router
from routers.web.about import about_router
from routers.web.users import users_router
from routers.web.categories import categories_router
from routers.web.topic import topic_router
from routers.web.messenger import messenger_router
from routers.web.conversation import conversation_router


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_category_router)
app.include_router(api_topic_router)
app.include_router(api_users_router)
app.include_router(api_reply_router)
app.include_router(api_message_router)
app.include_router(api_conversation_router)
app.include_router(index_router)
app.include_router(users_router)
app.include_router(about_router)
app.include_router(categories_router)
app.include_router(access_router)
app.include_router(topic_router)
app.include_router(messenger_router)    
app.include_router(conversation_router)

# TODO NO CATEGORIES TO SHOW OR NO TOPICS TO SHOW MESSAGE IN THE TEMPLATES
# TODO MAKE HOME PAGE UNIQUE 

if __name__ == "__main__":
    uvicorn.run('main:app')


# todo remove all verbs