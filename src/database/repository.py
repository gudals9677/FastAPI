from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo, User

class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_todos(self) -> List[ToDo]:
        return list(self.session.scalars(select(ToDo)))

    def get_todo_by_todo_id(self, todo_id: int) -> Optional[ToDo]:
        return self.session.scalars(select(ToDo).where(ToDo.id == todo_id)).first()  # ✅ .first() 추가

    def create_todo(self, todo: ToDo) -> ToDo:
        self.session.add(todo)  # ✅ instance=todo 대신 todo만 추가
        self.session.commit()
        self.session.refresh(todo)  # ✅ DB 반영
        return todo

    def update_todo(self, todo: ToDo) -> ToDo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(ToDo).where(ToDo.id == todo_id))
        self.session.commit()
