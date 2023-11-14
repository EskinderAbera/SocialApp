from fastapi import FastAPI
import uvicorn

from db.db import engine
from endpoints.post_endpoints import post_router
from endpoints.user_endpoints import user_router
from models.post_models import *

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    # create_db_and_tables()
    uvicorn.run('main:app', host="localhost", port=5000, reload=True)
