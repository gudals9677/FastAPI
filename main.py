from typing import List

from fastapi import FastAPI, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
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

    if todo:
        return ToDoSchema.from_orm(todo)
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# POST API
@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db),
    ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo)
    return ToDoSchema.from_orm(todo)

# PATCH API
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db)
    ):
    todo: ToDo = get_todo_by_todo_id(session=session, todo_id=todo_id)
    # todo check 후 ToDo가 존재한다면 Update
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# DELETE API
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db)
):
    todo: ToDo = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    # 삭제 함수 호출
    delete_todo(session=session, todo_id=todo_id)