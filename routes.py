from fastapi import APIRouter, Request, Depends, Path
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services.todo_service import TodoService
from app.services.user_service import UserService
from app.controllers.todo_controller import TodoController
from app.controllers.auth_controller import AuthController
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema

router = APIRouter()

todo_service = TodoService()
user_service = UserService()

todo_controller = TodoController(todo_service)
auth_controller = AuthController(user_service)

# -----------------------------------------------------
# LOGIN
# -----------------------------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return auth_controller.login(db, form_data)

# -----------------------------------------------------
# LIST TODOS (WITH FILTERS)
# -----------------------------------------------------
@router.get("/todo/list")
def list_todos(
    request: Request,
    db: Session = Depends(get_db)
):
    return todo_controller.list_todos(db, request)

# -----------------------------------------------------
# LIST ASSIGNEES
# -----------------------------------------------------
@router.get("/assignee")
def list_assignee(
    db: Session = Depends(get_db)
):
    return todo_controller.list_assignee(db)

# -----------------------------------------------------
# CREATE TODO
# -----------------------------------------------------
@router.post("/todo")
def create_todo(
    todo_data: TodoCreateSchema,
    db: Session = Depends(get_db)
):
    return todo_controller.create(todo_data, db)

# -----------------------------------------------------
# GET TODO BY UUID
# -----------------------------------------------------
@router.get("/todo/{todo_uuid}")
def show_todo(
    todo_uuid: str = Path(..., description="UUID of the todo"),
    db: Session = Depends(get_db)
):
    return todo_controller.get_by_uuid(todo_uuid, db)

# -----------------------------------------------------
# UPDATE TODO BY UUID
# -----------------------------------------------------
@router.put("/todo/{todo_uuid}")
def update_todo(
    todo_uuid: str,
    todo_data: TodoUpdateSchema,
    db: Session = Depends(get_db)
):
    return todo_controller.update(
        todo_uuid,
        todo_data.model_dump(exclude_unset=True),  # ✅ FIX
        db
    )

# -----------------------------------------------------
# DELETE TODO (SOFT DELETE) BY UUID
# -----------------------------------------------------
@router.delete("/todo/{todo_uuid}")
def delete_todo(
    todo_uuid: str,
    db: Session = Depends(get_db)
):
    return todo_controller.delete(todo_uuid, db)

# -----------------------------------------------------
# REVOKE TODO BY UUID
# -----------------------------------------------------
@router.put("/todo/{todo_uuid}/revoke")
def revoke_todo(
    todo_uuid: str,
    db: Session = Depends(get_db)
):
    return todo_controller.revoke(todo_uuid, db)
