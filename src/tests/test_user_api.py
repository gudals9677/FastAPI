from database.orm import User
from database.repository import UserRepository
from service.user import UserService


def test_user_sign_up(client, mocker):
    hash_password = mocker.patch.object(
        UserService,
        "hash_password",
        return_value = "hashed",
    )
    user_create = mocker.patch.object(
        User,
        "create",
        return_value=User(id=None, username="test", password="hashed"),
    )
    mocker.patch.object(
        UserRepository,
        "save_user",
        return_value = User()
    )

    body = {
        "username": "test",
        "password": "plain",
    }
    resource = client.post("/user/sign-up", json=body)

    # hash_password 함수 mocking
    hash_password.assert_called_once_with("plain")
    # user_create 함수 mocking
    user_create.assert_called_once_with("test", "hashed")

    assert resource.status_code == 201
    assert resource.json() == {"id" : 1, "username": "test"}