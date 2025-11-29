from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.todo_service import TodoService
from app.controllers.todo_controller import TodoController
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema

router = APIRouter(prefix="/todos", tags=["Todos"])

todo_service = TodoService()
todo_controller = TodoController(todo_service)

# -----------------------------------------------------
# LIST WITH FILTERS
# -----------------------------------------------------
@router.get("/")
def list_todos(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    status: str = Query(None, description="pending, in-progress, completed"),
    priority: str = Query(None, description="low, medium, high"),
    user_id: int = Query(None),
    start_date: str = Query(None, description="Start date for filtering"),
    end_date: str = Query(None, description="End date for filtering")
):
    return todo_controller.list_todos(
        db=db,
        offset=offset,
        limit=limit,
        status=status,
        priority=priority,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

# -----------------------------------------------------
# LIST ASSIGNEES
# -----------------------------------------------------
@router.get("/assignee")
def list_assignee(db: Session = Depends(get_db)):
    return todo_controller.list_assignee(db)

# -----------------------------------------------------
# CREATE TODO
# -----------------------------------------------------
@router.post("/")
def create_todo(todo_data: TodoCreateSchema, db: Session = Depends(get_db)):
    return todo_controller.create(todo_data, db)

# -----------------------------------------------------
# GET SINGLE TODO
# -----------------------------------------------------
@router.get("/{todo_id}")
def show_todo(
    todo_id: int = Path(..., description="ID of the todo"),
    db: Session = Depends(get_db)
):
    return todo_controller.get_by_id(todo_id, db)

# -----------------------------------------------------
# UPDATE TODO
# -----------------------------------------------------
@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    todo_data: TodoUpdateSchema,
    db: Session = Depends(get_db)
):
    return todo_controller.update(todo_id, todo_data, db)

# -----------------------------------------------------
# DELETE TODO (SOFT DELETE)
# -----------------------------------------------------
@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    return todo_controller.delete(todo_id, db)

# -----------------------------------------------------
# REVOKE (change status to revoked)
# -----------------------------------------------------
@router.put("/{todo_id}/revoke")
def revoke_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    return todo_controller.revoke(todo_id, db)
