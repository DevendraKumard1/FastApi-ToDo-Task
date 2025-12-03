# app/seeders/user_seeder.py
import uuid

from app.models.user import User

def seed_users(db):
    users = [
        {"username": "Test User", "uuid": str(uuid.uuid4()), "email": "test.u@academixs.com"},
        {"username": "Saurabh Shukla", "uuid": str(uuid.uuid4()), "email": "saurabh.s@academixs.com"},
        {"username": "Devendra Kumar", "uuid": str(uuid.uuid4()), "email": "devendra.k@academixs.com"},
    ]

    for data in users:
        db.add(User(**data))

    db.commit()
    print("Users seeded successfully")
