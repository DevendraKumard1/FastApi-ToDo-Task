from Services.ToDoService import ToDoService
from fastapi import HTTPException
from app.schemas.ToDoSchema import ToDoCreateSchema, TodoResponse
from sqlalchemy.orm import Session

class ToDoController:
    
    def __init__(self, todoService: ToDoService):
        self.todoService = todoService
        
    def list_todos(self, db: Session):
        try:
            todo_record = self.todoService.get_todos(db)
            return todo_record
        except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")

    def create(self, todo_data: ToDoCreateSchema, db: Session):
        try:
            created_todo = self.todoService.insert_records(todo_data.dict(), db)
            
            if not created_todo:
                raise HTTPException(status_code=500, detail="Something went wrong while creating the todo")
            
            return TodoResponse.from_orm(created_todo)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")


