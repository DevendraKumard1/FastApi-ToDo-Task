# seeders/todo_seeder.py
from sqlalchemy.orm import Session
from app.models.User import User

def seed_users(db: Session):
    users = [
        {
            "username": "Devendra Kumar",
            "email": "devendra.k@academixs.com",
        },
        {
            "username": "Saurabh Shukla",
            "email": "saurabh.s@academixs.com",
        }
    ]

    for user in users:
        user = User(**user)
        db.add(user)
    
    db.commit()
    print(f"{len(users)} users seeded successfully!")
