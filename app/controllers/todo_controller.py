from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.todo_service import TodoService
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema, TodoResponse


class TodoController:

    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    # -----------------------------------
    # LIST TODOS (FILTER + PAGINATION)
    # -----------------------------------
    def list_todos(self, db: Session, request):
        try:
            query_params = dict(request.query_params)
            result = self.todo_service.get_todos(db, **query_params)

            return {
                "status": status.HTTP_200_OK,
                "message": "Todos fetched successfully",
                "total": result["total"],
                "offset": result["offset"],
                "limit": result["limit"],
                "result": result["data"]
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching todos: {e}"
            )

    # -----------------------------------
    # LIST ASSIGNEES
    # -----------------------------------
    def list_assignee(self, db: Session):
        try:
            assignees = self.todo_service.get_assignee(db)
            return {
                "status": status.HTTP_200_OK,
                "message": "Assignee fetched successfully",
                "result": assignees
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching assignees: {e}"
            )

    # -----------------------------------
    # CREATE TODO
    # -----------------------------------
    def create(self, todo_data: TodoCreateSchema, db: Session):
        try:
            payload = todo_data.model_dump()
            todo = self.todo_service.insert_todo(payload, db)

            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create todo"
                )

            return TodoResponse.model_validate(todo)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating todo: {e}"
            )

    # -----------------------------------
    # UPDATE TODO
    # -----------------------------------
    def update(self, todo_id: int, todo_data: TodoUpdateSchema, db: Session):
        try:
            # Check if todo_data is a dict or Pydantic model
            if isinstance(todo_data, dict):
                payload = todo_data
            else:
                payload = todo_data.model_dump(exclude_unset=True)
            
            # Call your service to update the todo
            todo = self.todo_service.update_todo(todo_id, payload, db)

            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Todo not found"
                )

            return {
                "status": status.HTTP_200_OK,
                "message": "Todo updated successfully",
                "result": TodoResponse.model_validate(todo)
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating todo: {e}"
            )
            
    # -----------------------------------
    # REVOKE TODO
    # -----------------------------------
    def revoke(self, todo_id: int, db: Session):
        try:
            todo = self.todo_service.revoke_todo(todo_id, db)

            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Todo not found"
                )

            return {
                "status": status.HTTP_200_OK,
                "message": "Todo revoked successfully",
                "result": TodoResponse.model_validate(todo)
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error revoking todo: {e}"
            )
