from app.models.ToDo import ToDo
from app.models.User import User
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
import uuid

class ToDoService:
   
    def get_todos(self, db, offset, limit):
        query = (
            db.query(ToDo)
            .options(joinedload(ToDo.user, innerjoin=True))
            .order_by(desc(ToDo.created_at))
            .offset(offset)
            .limit(limit)
        )
        todos = query.all()
        total = db.query(ToDo).count()

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "data": todos
        }
    
    def get_assignee(self, db):
        return db.query(User).all()
    
    def insert_records(self, data: dict, db):
        data["uuid"] = str(uuid.uuid4())
        new_todo = ToDo(**data)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return new_todo