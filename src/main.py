from fastapi import FastAPI, HTTPException, Depends, Body
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import ToDoRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "Hello World"}


@app.get("/todos", status_code=200)
def get_todos_handler(
        order: str = "ASC",
        session: Session = Depends(get_db),
) -> ToDoListSchema:
    todo_repo = ToDoRepository(session)  #  Repository 객체 생성
    todos = todo_repo.get_todos()  #  Repository를 이용해 데이터 가져오기

    if order == "DESC":
        todos = todos[::-1]

    return ToDoListSchema(
        todos=[ToDoSchema.from_orm(todo) for todo in todos]
    )


# GET API (단일 조회)
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo_repo = ToDoRepository(session)
    todo = todo_repo.get_todo_by_todo_id(todo_id)

    if todo:
        return ToDoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="ToDo Not Found")


# POST API (할 일 추가)
@app.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        session: Session = Depends(get_db),
):
    todo_repo = ToDoRepository(session)
    todo = ToDo(**request.dict())  # request 데이터로 ToDo 객체 생성
    todo = todo_repo.create_todo(todo)
    return ToDoSchema.from_orm(todo)


# PATCH API (할 일 업데이트)
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
):
    todo_repo = ToDoRepository(session)
    todo = todo_repo.get_todo_by_todo_id(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    todo.is_done = is_done
    todo = todo_repo.update_todo(todo)
    return ToDoSchema.from_orm(todo)


# DELETE API (할 일 삭제)
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        session: Session = Depends(get_db),
):
    todo_repo = ToDoRepository(session)
    todo = todo_repo.get_todo_by_todo_id(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    todo_repo.delete_todo(todo_id)
