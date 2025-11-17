from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from Services.ToDoService import ToDoService
from Controllers.ToDoController import ToDoController
from app.schemas.ToDoSchema import ToDoCreateSchema

router = APIRouter()

todo_service = ToDoService()
todo_controller = ToDoController(todo_service) 

# ToDo routes
@router.get("/")
def list_todos(db: Session = Depends(get_db), offset: int = Query(0, ge=0), limit: int = Query(10, ge=1) ):
    return todo_controller.list_todos(db, offset, limit)

@router.get("/assignee")
def list_assignee(db: Session = Depends(get_db)):
    return todo_controller.list_assignee(db)

@router.post("/todo")
def create_todo(todo_data: ToDoCreateSchema, db: Session = Depends(get_db)):
    return todo_controller.create(todo_data, db)