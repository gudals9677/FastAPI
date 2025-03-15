from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()

# TEST API
@app.get("/")
def health_check():
    return {"message": "Hello World"}

todo_data = {
    1: {
        "todo_id": 1,
        "contents": "Test FastAPI",
        "is_done": True,
    },
    2: {
        "todo_id": 2,
        "contents": "Test FastAPI",
        "is_done": False,
    },
    3: {
        "todo_id": 3,
        "contents": "Test FastAPI",
        "is_done": False,
    },
}

# GET API(전체 조회)
@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str,
        session: Session = Depends(get_db),
) -> ToDoListSchema:
    todos: List[ToDo] = get_todos(session=session)
    if order == "DESC":
        return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos]
    )

# GET API(단일 조회)
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo: ToDo = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if ToDoSchema:
        return [ToDoSchema.from_orm(todo)]
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="Not Found")

# POST API
@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.todo_id] = request.dict()
    return todo_data[request.todo_id]

# PATCH API
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Not Found")

# DELETE API
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int):
    # pop = id 값을 제거하고 반환
    todo = todo_data.pop(todo_id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="Not Found")
