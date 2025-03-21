from database.orm import ToDo
from database.repository import ToDoRepository

# api 요청에 대한 테스트 코드를 작성

def test_get_todos(client, mocker):
    # order asc

    # api.todo.py get_todos 함수를 mocking
    mocker.patch.object(ToDoRepository, "get.todos", return_value=[
        ToDo(id=1, contents="FastAPI Section 0", is_done=True),
        ToDo(id=2, contents="FastAPI Section 1", is_done=False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos" :[
            {"id" : 1, "contents" : "FastAPI Section 0", "is done" : True},
            {"id" : 2, "contents" : "FastAPI Section 1", "is done" : False},
        ]
    }

    # order desc
    response = client.get("/todos?Order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [
            {"id": 3, "contents": "FastAPI Section 2", "is done": True},
            {"id": 2, "contents": "FastAPI Section 1", "is done": True},
            {"id": 1, "contents": "FastAPI Section 0", "is done": True},
        ]
    }

def test_get_todo(client, mocker):
    # 200
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))

    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {"id":1, "contents":"todo", "is_done":True}

    # 404
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=None)

    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}

def test_create_todo(client, mocker):
    # api.todo.py ToDo.create 함수에 대한 response data 검증
    create_spy = mocker.spy(ToDo, "create")

    mocker.patch.object(ToDoRepository,"create_todo", return_value=ToDo(id=1, contents="todo", is_done=True))

    body = {
        "contents" : "Test",
        "is_done" : False
    }
    response = client.post("/todos", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "Test"
    assert create_spy.spy_return.is_done is False

    assert response.status_code == 201
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

def test_update_todo(client, mocker):
    # 200
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))
    undone = mocker.patch.object(ToDo, "undone")
    mocker.patch.object(ToDoRepository,"update_todo", return_value=ToDo(id=1, contents="todo", is_done=False))

    response = client.patch("/todos?1", json={"is_done" : False})

    undone.assert_called_once_with()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "contents": "todo", "is_done": True}

    # 404
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=None)

    response = client.patch("/todos/1", json={"is_done" : False})
    assert response.status_code == 404
    assert response.json() == {"detail": "ToDo Not Found."}

def test_delete_todo(client, mocker):
    # 200
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=ToDo(id=1, contents="todo", is_done=True))
    mocker.patch.object(ToDoRepository,"delete_todo", return_value=None)

    response = client.get("/todos/1")
    assert response.status_code == 204

    # 404
    mocker.patch.object(ToDoRepository,"get_todo_by_todo_id", return_value=None)

    response = client.delete("/todos/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}