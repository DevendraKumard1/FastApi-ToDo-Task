from fastapi import APIRouter, Request, Depends, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.todo_service import TodoService
from app.services.user_service import UserService
from app.controllers.todo_controller import TodoController
from app.controllers.auth_controller import AuthController
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

todo_service = TodoService()
user_service = UserService()
todo_controller = TodoController(todo_service)
auth_controller = AuthController(user_service)

# -----------------------------------------------------
# Login route
# -----------------------------------------------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_controller.login(db, form_data)

# -----------------------------------------------------
# LIST WITH FILTERS
# -----------------------------------------------------
@router.get("/todo/list")
def list_todos(request: Request, db: Session = Depends(get_db)):
    return todo_controller.list_todos(db, request)

# -----------------------------------------------------
# LIST ASSIGNEES
# -----------------------------------------------------
@router.get("/assignee")
def list_assignee(db: Session = Depends(get_db)):
    return todo_controller.list_assignee(db)

# -----------------------------------------------------
# CREATE TODO
# -----------------------------------------------------
@router.post("/todo")
def create_todo(todo_data: TodoCreateSchema, db: Session = Depends(get_db)):
    return todo_controller.create(todo_data, db)

# -----------------------------------------------------
# GET SINGLE TODO
# -----------------------------------------------------
@router.get("/todo/{todo_id}")
def show_todo(
    todo_id: int = Path(..., description="ID of the todo"),
    db: Session = Depends(get_db)
):
    return todo_controller.get_by_id(todo_id, db)

# -----------------------------------------------------
# UPDATE TODO
# -----------------------------------------------------
@router.put("/todo/{todo_id}")
def update_todo(
    todo_id: int,
    todo_data: TodoUpdateSchema,
    db: Session = Depends(get_db)
):
    return todo_controller.update(todo_id, todo_data, db)

# -----------------------------------------------------
# DELETE TODO (SOFT DELETE)
# -----------------------------------------------------
@router.delete("todo/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    return todo_controller.delete(todo_id, db)

# -----------------------------------------------------
# REVOKE (change status to revoked)
# -----------------------------------------------------
@router.put("/todo/{todo_id}/revoke")
def revoke_todo(
    todo_id: int, 
    db: Session = Depends(get_db)
):
    return todo_controller.revoke(todo_id, db)
