from Services.ToDoService import ToDoService

class ToDoController:
    
    def __init__(self, todoService: ToDoService):
        self.todoService = todoService
        
    def list_todos(self):
        service_data = self.todoService.get_todos()
        return {"todos": service_data}

    def create():
        return {"message": "creating a todo"}


