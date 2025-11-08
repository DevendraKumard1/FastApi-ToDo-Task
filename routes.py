from fastapi import APIRouter
from Services.ToDoService import ToDoService
from Controllers.ToDoController import ToDoController

router = APIRouter()

todo_service = ToDoService()
todo_controller = ToDoController(todo_service) 

def list_todos():
    return todo_controller.list_todos()

# ToDo routes
router.get("/")(todo_controller.list_todos)
router.post("/todo")(todo_controller.create)
