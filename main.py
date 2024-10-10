from fastapi import FastAPI
from routers.category import category_router


app = FastAPI()
app.include_router(category_router)