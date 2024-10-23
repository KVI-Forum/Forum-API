from fastapi import FastAPI
from routers.category import category_router
from routers.reply import reply_router
from routers.topic import topic_router
from routers.user import users_router
from routers.message import message_router
from routers.conversation import conversation_router
from routers.vote import vote_router

app = FastAPI()
app.include_router(category_router)
app.include_router(topic_router)
app.include_router(users_router)
app.include_router(reply_router)
app.include_router(message_router)
app.include_router(conversation_router)
app.include_router(vote_router)






# TODO: Add new columns to the categories table to indicate:
#       - Whether the category is private
#       - Whether the category is locked        !!! DONE 

# TODO: Add an option to lock topics in the system.

# TODO: Refactor the following components to implement access-related changes:
#       - Topic reply
#       - Category services
#       - Routers
#       - Topic service
#       - Reply service
#       - User service

# TODO: Modify the access table to include: !!! DONE
#       - Read access
#       - Write access



