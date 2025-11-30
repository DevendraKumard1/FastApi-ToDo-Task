from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Optional
from app.models.todo import Todo
from app.models.user import User
import uuid

class TodoService:
    def get_todos(
        self,
        db: Session,
       **filters
    ):
        offset = filters.get("offset") or 0
        limit = filters.get("limit") or 10
        query = db.query(Todo).options(joinedload(Todo.user, innerjoin=True))

        if filters.get("titleFilter"):
            query = query.filter(Todo.title.ilike(f"%{filters['titleFilter']}%"))
        if filters.get("assigneeFilter"):
            query = query.filter(Todo.user_id == filters["assigneeFilter"])
        if filters.get("statusFilter"):
            query = query.filter(Todo.status == filters["statusFilter"])
        if filters.get("priorityFilter"):
            query = query.filter(Todo.priority == filters["priorityFilter"])
        if filters.get("scheduledDateFilter"):
            query = query.filter(Todo.scheduled_date == filters["scheduledDateFilter"])

        total = query.count()
        query = query.order_by(desc(Todo.created_at)).offset(offset).limit(limit)
        todos = query.all()

        return {
            "total": total,
            "offset":  offset,
            "limit":  limit,
            "data": todos
        }

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
