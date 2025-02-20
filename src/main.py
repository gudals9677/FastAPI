from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()

# TEST API
@app.get("/")
def health_check():
    return {"message": "Hello World"}

todo_data = {
    1: {
        "id": 1,
        "contents": "Test FastAPI",
        "is_done": True,
    },
    2: {
        "id": 2,
        "contents": "Test FastAPI",
        "is_done": False,
    },
    3: {
        "id": 3,
        "contents": "Test FastAPI",
        "is_done": False,
    },
}

# GET API(전체 조회)
@app.get("/todos", status_code=200)
def get_todos_handler(order: str):
    # todo_data values push to List
    ret = list(todo_data.values())
    if order == "DESC":
        return ret[::-1]
    return ret

# GET API(단일 조회)
@app.get("/todos/{todos_id}", status_code=200)
def get_todo_handler(id: int):
    todo = todo_data.get(id)
    if todo:
        return todo
    # HTTP STATUS CODE 반환 값 지정(import HTTPException)
    raise HTTPException(status_code=404, detail="Not Found")

# RequestBody 대체(import BaseModel)
class CreateToDoRequest(BaseModel):
    id:int
    contents: str
    is_done: bool

# POST API
@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]

# PATCH API
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        id: int,
        is_done: bool = Body(..., embed=True),
):
    todo = todo_data.get(id)
    if todo:
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="Not Found")

# DELETE API
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(id: int):
    # pop = id 값을 제거하고 반환
    todo = todo_data.pop(id, None)
    if todo:
        return
    raise HTTPException(status_code=404, detail="Not Found")
