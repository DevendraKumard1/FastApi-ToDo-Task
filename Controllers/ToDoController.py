from Services.ToDoService import ToDoService
from fastapi import HTTPException
from app.schemas.ToDoSchema import ToDoCreateSchema, TodoResponse
from sqlalchemy.orm import Session
import pendulum

class ToDoController:
    
    def __init__(self, todoService: ToDoService):
        self.todoService = todoService
        
    def list_todos(self, db: Session, offset, limit):
        try:
            todo_record = self.todoService.get_todos(db, offset, limit)

            todos_list = todo_record["data"]
            formatted_todos = []
            for todo in todos_list:
                formatted_date = ""
                if todo.scheduled_date:
                    dt = pendulum.instance(todo.scheduled_date)
                    day = dt.day
                    formatted_date = f"{day} {dt.format('MMM YYYY').capitalize()}"

                formatted_priority = todo.priority.capitalize() if todo.priority else ""
                formatted_status = todo.status.capitalize() if todo.status else ""

                formatted_todo = todo.__dict__.copy()
                formatted_todo["formatted_date"] = formatted_date
                formatted_todo["formatted_priority"] = formatted_priority
                formatted_todo["formatted_status"] = formatted_status
                formatted_todos.append(formatted_todo)

            return {
                "status": 200,
                "message": "Todos fetched successfully",
                "total": todo_record["total"],
                "offset": todo_record["offset"],
                "limit": todo_record["limit"],
                "result": formatted_todos
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching todos: {e}")
    
    def list_assignee(self, db: Session):
        try:
            assignee = self.todoService.get_assignee(db)
            return {
                "status": 200,
                "message": "Assignee fetched successfully",
                "result": assignee
            }
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


