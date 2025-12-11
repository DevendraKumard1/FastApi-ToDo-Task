# app/seeders/user_seeder.py
import uuid

from app.models.user import User
from app.services.auth_service import hash_password

def seed_users(db):
    users = [
        {"username": "Test User", "uuid": str(uuid.uuid4()), "email": "test.u@academixs.com", "password": hash_password("Tech@123")},
        {"username": "Saurabh Shukla", "uuid": str(uuid.uuid4()), "email": "saurabh.s@academixs.com", "password": hash_password("Tech@123")},
        {"username": "Devendra Kumar", "uuid": str(uuid.uuid4()), "email": "devendra.k@academixs.com", "password": hash_password("Tech@123")},
    ]

    for data in users:
        db.add(User(**data))

    db.commit()
    print("Users seeded successfully")
