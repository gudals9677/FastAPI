import bcrypt
from datetime import datetime, timedelta
from jose import jwt

class UserService:
    encoding: str = "utf-8"
    secret_key: str = "7462a2ecd932349866954f3072c7e499b48a600ad30bfae5736ae80aa647c8ddex"
    jwt_algorithm: str = "HS256"

    # 패스워드 암호화 작업
    def hash_password(self, plain_password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            plain_password.encode(self.encoding),
            salt=bcrypt.gensalt()
        )
        return hashed_password.decode(self.encoding)

    def verify_password(
            self, plain_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(self.encoding),
            hashed_password.encode(self.encoding)
        )

    # jwt token 생성
    def create_jwt(
            self,
            username: str
    ) -> str:
        return jwt.encode({
            "sub" : username,
            "exp" : datetime.now() + timedelta(days=1),
        },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )

    def decode_jwt(self,access_token: str):
        payload = jwt.decode(
            access_token, self.secret_key,
            algorithms=[self.jwt_algorithm]
        )
        return payload["sub"]