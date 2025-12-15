from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import Optional
from app.models.todo import Todo
from app.models.user import User
from sqlalchemy.sql import func
import uuid


class TodoService:

    # -------------------------
    # LIST TODOS (FILTER + PAGINATION)
    # -------------------------
    def get_todos(self, db: Session, **filters):
        offset = int(filters.get("offset", 0))
        limit = int(filters.get("limit", 10))

        query = db.query(Todo).options(
            joinedload(Todo.user, innerjoin=True)
        ).filter(
            Todo.deleted_at.is_(None)
        )

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

        todos = (
            query
            .order_by(desc(Todo.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "data": todos
        }

    # -------------------------
    # CREATE TODO
    # -------------------------
    def insert_todo(self, payload: dict, db: Session) -> Todo:
        payload["uuid"] = str(uuid.uuid4())
        todo = Todo(**payload)

        db.add(todo)
        db.commit()
        db.refresh(todo)

        return todo

    # -------------------------
    # GET TODO BY UUID
    # -------------------------
    def get_by_uuid(self, todo_uuid: str, db: Session) -> Optional[Todo]:
        return (
            db.query(Todo)
            .filter(
                Todo.uuid == todo_uuid,
                Todo.deleted_at.is_(None)
            )
            .first()
        )

    # -------------------------
    # UPDATE TODO BY UUID
    # -------------------------
    def update_todo(self, todo_uuid: str, payload: dict, db: Session) -> Optional[Todo]:
        todo = self.get_by_uuid(todo_uuid, db)
        if not todo:
            return None

        for key, value in payload.items():
            if hasattr(todo, key) and value is not None:
                setattr(todo, key, value)

        db.commit()
        db.refresh(todo)
        return todo


    # -------------------------
    # REVOKE TODO
    # -------------------------
    def revoke_todo(self, todo_uuid: str, db: Session) -> Optional[Todo]:
        todo = self.get_by_uuid(todo_uuid, db)
        if not todo:
            return None

        todo.status = "revoked"
        db.commit()
        db.refresh(todo)

        return todo

    # -------------------------
    # SOFT DELETE TODO
    # -------------------------
    def soft_delete(self, todo_uuid: str, db: Session) -> Optional[Todo]:
        todo = self.get_by_uuid(todo_uuid, db)
        if not todo:
            return None

        todo.deleted_at = func.now()
        db.commit()
        db.refresh(todo)

        return todo

    # -------------------------
    # ASSIGN TODO TO USER
    # -------------------------
    def assign_to_user(self, todo_uuid: str, user_id: int, db: Session) -> Optional[Todo]:
        todo = self.get_by_uuid(todo_uuid, db)
        user = db.query(User).filter(User.id == user_id).first()

        if not todo or not user:
            return None

        todo.user_id = user_id
        db.commit()
        db.refresh(todo)

        return todo

    # -------------------------
    # LIST ASSIGNEES
    # -------------------------
    def get_assignee(self, db: Session):
        return db.query(User).all()
