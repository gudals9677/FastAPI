from typing import List

from fastapi import Depends, HTTPException, Body, APIRouter

from database.orm import ToDo, User
from database.repository import ToDoRepository, UserRepository
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema
from security import get_access_token
from service.user import UserService

router = APIRouter()

@router.get("/")
def health_check_handler():
    return {"ping": "pong"}

@router.get("/todos", status_code=200)
def get_todos_handler(
        access_token: str = Depends(get_access_token),
        order: str | None = None,
        user_service: UserService = Depends(),
        todo_repo: ToDoRepository = Depends(),
        user_repo: UserRepository = Depends(),
) -> ToDoListSchema:

    username: str = user_service.decode_jwt(access_token = access_token)

    user: User | None = user_repo.get_by_username(username = username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    todos: List[ToDo] = user.todos
    if order == "DESC":
        return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos[::-1]]
    )
    return ToDoListSchema(
        todos = [ToDoSchema.from_orm(todo) for todo in todos]
    )


@router.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
        todo_id: int,
        todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: ToDo = todo_repo.get_todo_by_todo_id()

    if todo:
        return ToDoSchema.from_orm(todo)
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.post("/todos", status_code=201)
def create_todo_handler(
        request: CreateToDoRequest,
        todo_repo: ToDoRepository = Depends(ToDoRepository),
    ) -> ToDoSchema:
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = todo_repo.create_todo()
    return ToDoSchema.from_orm(todo)


@router.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        todo_repo: ToDoRepository = Depends(ToDoRepository),
    ):
    todo: ToDo = todo_repo.get_todo_by_todo_id()
    # todo check 후 ToDo가 존재한다면 Update
    if todo:
        # update
        todo.done() if is_done else todo.undone()
        todo: ToDo = todo_repo.update_todo()
        return ToDoSchema.from_orm(todo)
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="ToDo Not Found")


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
        todo_id: int,
        todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: ToDo = todo_repo.get_todo_by_todo_id()

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo Not Found")

    # 삭제 함수 호출
    todo_repo.delete_todo()
