from fastapi import FastAPI
from api import todo
app = FastAPI()
app.include_router(todo.router)

# TEST API

# GET API(전체 조회)

# GET API(단일 조회)

# POST API

# PATCH API

# DELETE API
