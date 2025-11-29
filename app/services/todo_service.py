from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_
from typing import Optional
from app.models.todo import Todo
from app.models.user import User
from datetime import date, datetime
import uuid

class TodoService:
    def get_todos(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 10,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        user_id: Optional[int] = None,
        search: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_deleted: bool = False,
    ):
        """
        Returns dict: { total, offset, limit, data }
        """
        q = db.query(Todo)

        if not include_deleted:
            q = q.filter(Todo.deleted_at.is_(None))

        if status:
            q = q.filter(Todo.status == status)

        if priority:
            q = q.filter(Todo.priority == priority)

        if user_id:
            q = q.filter(Todo.user_id == user_id)

        if start_date and end_date:
            q = q.filter(Todo.scheduled_date.between(start_date, end_date))
        elif start_date:
            q = q.filter(Todo.scheduled_date >= start_date)
        elif end_date:
            q = q.filter(Todo.scheduled_date <= end_date)

        if search:
            like = f"%{search}%"
            q = q.filter(or_(Todo.title.ilike(like), Todo.description.ilike(like)))

        total = q.with_entities(func.count()).scalar() or 0

        q = q.order_by(Todo.scheduled_date.desc(), Todo.created_at.desc()).offset(offset).limit(limit)
        results = q.all()

        return {"total": total, "offset": offset, "limit": limit, "data": results}

    def insert_records(self, payload: dict, db: Session) -> Todo:
        # Generate UUID for new todo
        payload['uuid'] = str(uuid.uuid4())
        todo = Todo(**payload)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def update_todo(self, todo_id: int, payload: dict, db: Session) -> Optional[Todo]:
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.deleted_at.is_(None)).first()
        if not todo:
            return None

        for k, v in payload.items():
            if hasattr(todo, k) and v is not None:
                setattr(todo, k, v)

        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def delete_todo(self, todo_id: int, db: Session, hard: bool = False) -> bool:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return False

        if hard:
            db.delete(todo)
            db.commit()
            return True

        # Soft delete
        todo.deleted_at = datetime.utcnow()
        db.add(todo)
        db.commit()
        return True

    def revoke_todo(self, todo_id: int, db: Session) -> Optional[Todo]:
        # Mark the todo as revoked by updating status
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.deleted_at.is_(None)).first()
        if not todo:
            return None
        todo.status = "revoked"
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def assign_todo_to_user(self, todo_id: int, user_id: int, db: Session) -> Optional[Todo]:
        # Assign a todo to a user
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.deleted_at.is_(None)).first()
        user = db.query(User).filter(User.id == user_id).first()
        if not todo or not user:
            return None
        todo.user_id = user_id
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def create_todo(self, payload: dict, db: Session) -> Todo:
        # Generate UUID and create new todo
        payload['uuid'] = str(uuid.uuid4())
        todo = Todo(**payload)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    def get_todo_by_uuid(self, uuid_str: str, db: Session) -> Optional[Todo]:
        return db.query(Todo).filter(Todo.uuid == uuid_str, Todo.deleted_at.is_(None)).first()

    def get_todo_by_id(self, todo_id: int, db: Session) -> Optional[Todo]:
        return db.query(Todo).filter(Todo.id == todo_id, Todo.deleted_at.is_(None)).first()

    def get_assignee(self, db):
        return db.query(User).all()
