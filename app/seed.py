# app/seed.py

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.todo import Todo

from app.seeders.user_seeder import seed_users
from app.seeders.todo_seeder import seed_todos

def run_seeders():
    db = SessionLocal()

    print("⏳ Seeding started...")

    seed_users(db)   # must run first
    seed_todos(db)   # run second

    db.close()
    print("🎉 All seeders executed successfully!")

if __name__ == "__main__":
    run_seeders()
