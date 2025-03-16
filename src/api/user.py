from http.client import HTTPException

from fastapi import APIRouter,Depends

from database.orm import User
from database.repository import UserRepository
from schema.request import SignUpRequest, LoginRequest
from schema.response import UserSchema, JWTResponse
from service.user import UserService

router = APIRouter(prefix="/users")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
        request: SignUpRequest,
        user_service: UserService = Depends(),
        user_repo : UserRepository = Depends(),
):
    # password hashing 작업
    hashed_password: str = user_service.hash_password(plain_password = request.password)

    # User 객체 생성
    user: User = User.create(user_name=request.username, hashed_password=hashed_password)

    # User 객체 db에 save (UserRepository 참조)
    user: User = user_repo.save_user(user=user)

    # User return
    return UserSchema.from_orm(user)

@router.post("/log-in")
def user_log_in_handler(
        request: LoginRequest,
        user_service: UserService = Depends(),
        user_repo : UserRepository = Depends(),
):
    # user가 db에 존재하는지 check
    user: User | None = user_repo.get_user_by_username(username=request.username)

    # user가 존재하지않으면 404 반환
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # user 패스워드 검증
    verified: bool = user_service.verify_password(
        plain_password = request.password,
        hashed_password = user.password,
    )
    # 패스워드 불일치 시 401 반환
    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")

    # 만약 모든 검증 통과 시 access_token 생성하여 반환(유효기간 1일)
    access_token: str = user_service.create_jwt(username=user.username)
    return JWTResponse(access_token=access_token)