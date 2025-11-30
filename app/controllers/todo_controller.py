from app.services.todo_service import TodoService
from fastapi import HTTPException
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema, TodoResponse
from sqlalchemy.orm import Session

class TodoController:
    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    # ------------------------------
    # LIST WITH FILTERS + PAGINATION
    # ------------------------------
    def list_todos(
        self,
        db: Session,
        request
    ):
        try:
            # Fetch todos from service
            query_params = dict(request.query_params)
            todo_record = self.todo_service.get_todos(db, **query_params)

            if not todo_record:
                raise HTTPException(status_code=404, detail="Records found")

            return {
                "status": 200,
                "message": "Todos fetched successfully",
                "total": todo_record["total"],
                "offset": todo_record["offset"],
                "limit": todo_record["limit"],
                "result": todo_record["data"]
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching todos: {e}")

    # ------------------------------
    # LIST ASSIGNEES (USERS)
    # ------------------------------
    def list_assignee(self, db: Session):
        try:
            assignee = self.todo_service.get_assignee(db)
            return {
                "status": 200,
                "message": "Assignee fetched successfully",
                "result": assignee
            }
        except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")

    # ------------------------------
    # CREATE TODO
    # ------------------------------
    def create(self, todo_data: TodoCreateSchema, db: Session):
        try:
            payload = todo_data.model_dump()
        
            created_todo = self.todo_service.insert_records(payload, db)
            if not created_todo:
                raise HTTPException(status_code=500, detail="Failed to create todo")
            return TodoResponse.model_validate(created_todo)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")

    # ------------------------------
    # UPDATE TODO
    # ------------------------------
    def update(self, todo_id: int, todo_data: TodoUpdateSchema, db: Session):
        try:
            payload = todo_data.model_dump(exclude_unset=True)
            updated_todo = self.todo_service.update_todo(todo_id, payload, db)

            if not updated_todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return {
                "status": 200,
                "message": "Todo updated successfully",
                "result": TodoResponse.model_validate(updated_todo)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating todo: {e}")

    # ------------------------------
    # REVOKE TODO (Change status to revoked)
    # ------------------------------
    def revoke(self, todo_id: int, db: Session):
        try:
            revoked_todo = self.todo_service.revoke(todo_id, db)
            return {
                "status": 200,
                "message": "Todo revoked successfully",
                "result": TodoResponse.model_validate(revoked_todo)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error revoking todo: {e}")


