from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from schema.request import CreateToDoRequest

Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    # ORM 객체로 변환
    @classmethod
    def create(cls, request: CreateToDoRequest):
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self) -> "ToDo":
        self.is_done = True
        return self

    def undone(self) -> "ToDo":
        self.is_done = False
        return self

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    todos = relationship("ToDo", lazy="joined") # User table 조회 시 ToDo 테이블도 조회되도록 연결

    # user 객체 생성 메소드
    @classmethod
    def create(cls, username: str, hashed_password: str) -> "User":
        return cls(
            username=username,
            password=hashed_password,
        )