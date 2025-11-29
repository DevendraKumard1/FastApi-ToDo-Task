# app/seeders/todo_seeder.py

from app.models.todo import Todo
import uuid
from datetime import date

def seed_todos(db):
    todos = [
        {
            "uuid": str(uuid.uuid4()),
            "user_id": 1,
            "title": "First Task",
            "scheduled_date": date.today(),
            "priority": "high",
            "status": "pending",
            "description": "This is a sample todo"
        },
        {
            "uuid": str(uuid.uuid4()),
            "user_id": 2,
            "title": "Second Task",
            "scheduled_date": date.today(),
            "priority": "medium",
            "status": "completed",
            "description": "Completed task example"
        }
    ]

    for data in todos:
        db.add(Todo(**data))

    db.commit()
    print("📌 Todos seeded successfully")
