from app.models.ToDo import ToDo
from app.models.User import User
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
import uuid

class TodoService:
   
    def get_todos(self, db, offset, limit):

        query = db.query(ToDo).options(joinedload(ToDo.user, innerjoin=True))

        # if filters.get("titleFilter"):
        #     query = query.filter(ToDo.title.ilike(f"%{filters['titleFilter']}%"))
        # if filters.get("assigneeFilter"):
        #     query = query.filter(ToDo.user_id == filters["assigneeFilter"])
        # if filters.get("statusFilter"):
        #     query = query.filter(ToDo.status == filters["statusFilter"])
        # if filters.get("priorityFilter"):
        #     query = query.filter(ToDo.priority == filters["priorityFilter"])
        # if filters.get("scheduledDateFilter"):
        #     query = query.filter(ToDo.scheduled_date == filters["scheduledDateFilter"])
            
        total = query.count()
        query = query.order_by(desc(ToDo.created_at)).offset(offset).limit(limit)
        todos = query.all()

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