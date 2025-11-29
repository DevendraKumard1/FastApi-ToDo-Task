from app.services.todo_service import TodoService
from fastapi import HTTPException
from app.schemas.todo_schema import TodoCreateSchema, TodoUpdateSchema, TodoResponse
from sqlalchemy.orm import Session
import pendulum


class TodoController:
    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    # ------------------------------
    # LIST WITH FILTERS + PAGINATION
    # ------------------------------
    def list_todos(
        self,
        db: Session,
        offset: int,
        limit: int,
        status: str = None,
        priority: str = None,
        user_id: int = None,
        search: str = None,
        start_date: str = None,
        end_date: str = None
    ):
        try:
            # Parse start_date and end_date strings to date objects
            start_date_obj = None
            end_date_obj = None

            from pendulum import parse as pendulum_parse

            if start_date:
                try:
                    start_date_obj = pendulum_parse(start_date).date()
                except Exception:
                    start_date_obj = None  # Ignore invalid date

            if end_date:
                try:
                    end_date_obj = pendulum_parse(end_date).date()
                except Exception:
                    end_date_obj = None

            # Fetch todos from service
            todo_record = self.todo_service.get_todos(
                db=db,
                offset=offset,
                limit=limit,
                status=status,
                priority=priority,
                user_id=user_id,
                search=search,
                start_date=start_date_obj,
                end_date=end_date_obj
            )

            todos_list = todo_record["data"]
            formatted_todos = []

            for todo in todos_list:
                formatted_date = ""
                if todo.scheduled_date:
                    dt = pendulum.instance(todo.scheduled_date)
                    formatted_date = f"{dt.day} {dt.format('MMM YYYY')}"

                # Prepare the todo dict
                formatted_todo = todo.__dict__.copy()

                # Safely add user info if exists
                user_info = getattr(todo, 'user', None)
                formatted_todo["user"] = {
                    "id": user_info.id,
                    "username": user_info.username,
                    "email": user_info.email,
                } if user_info else None

                # Add formatted fields for display
                formatted_todo["formatted_date"] = formatted_date
                formatted_todo["formatted_priority"] = todo.priority.capitalize()
                formatted_todo["formatted_status"] = todo.status.capitalize()

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
            payload = todo_data.dict()
            # Generate UUID
            import uuid
            payload['uuid'] = str(uuid.uuid4())

            created_todo = self.todo_service.insert_records(payload, db)
            if not created_todo:
                raise HTTPException(status_code=500, detail="Failed to create todo")
            return TodoResponse.from_orm(created_todo)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")

    # ------------------------------
    # UPDATE TODO
    # ------------------------------
    def update(self, todo_id: int, data: TodoUpdateSchema, db: Session):
        try:
            payload = data.dict(exclude_unset=True)
            updated_todo = self.todo_service.update_todo(todo_id, payload, db)
            if not updated_todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return {
                "status": 200,
                "message": "Todo updated successfully",
                "result": TodoResponse.from_orm(updated_todo)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating todo: {e}")

    # ------------------------------
    # DELETE TODO (SOFT DELETE)
    # ------------------------------
    def delete(self, todo_id: int, db: Session):
        try:
            deleted = self.todo_service.delete_todo(todo_id, db)
            if not deleted:
                raise HTTPException(status_code=404, detail="Todo not found")
            return {
                "status": 200,
                "message": "Todo deleted successfully"
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error deleting todo: {e}")

    # ------------------------------
    # REVOKE TODO (Change status to revoked)
    # ------------------------------
    def revoke(self, todo_id: int, db: Session):
        try:
            # Update status to 'revoked'
            revoked_todo = self.todo_service.update_todo(todo_id, {"status": "revoked"}, db)
            if not revoked_todo:
                raise HTTPException(status_code=404, detail="Todo not found")
            return {
                "status": 200,
                "message": "Todo revoked successfully",
                "result": TodoResponse.from_orm(revoked_todo)
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error revoking todo: {e}")
