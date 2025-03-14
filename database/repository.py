from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import ToDo

def get_todos(session: Session) -> List[ToDo]:
    return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session: Session, todo_id: int) -> Optional[ToDo]:
    return session.scalars(select(ToDo).where(ToDo.id == todo_id)).first()

def create_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit() # db commit
    session.refresh(instance=todo) # db read -> todo_id
    return todo

def update_todo(session: Session, todo: ToDo) -> ToDo:
    session.add(instance=todo)
    session.commit()  # db commit
    session.refresh(instance=todo)  # db read -> todo_id
    return todo

def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(delete(ToDo).where(ToDo.id == todo_id))
    session.commit()