from app.models.ToDo import ToDo
import uuid

class ToDoService:
   
    def get_todos(self, db):
        return db.query(ToDo).all()
    
    def insert_records(self, data: dict, db):
        data["uuid"] = str(uuid.uuid4())
        new_todo = ToDo(**data)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return new_todo