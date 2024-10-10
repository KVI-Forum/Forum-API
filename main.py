from fastapi import FastAPI
from routers.category import category_router
from routers.topic import topic_router

app = FastAPI()
app.include_router(category_router)
app.include_router(topic_router)