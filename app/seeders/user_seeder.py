# app/seeders/user_seeder.py

from app.models.user import User

def seed_users(db):
    users = [
        {"username": "Test User", "email": "test.u@academixs.com", "password": "123456"},
        {"username": "Saurabh Shukla", "email": "saurabh.s@academixs.com", "password": "123456"},
        {"username": "Devendra Kumar", "email": "devendra.k@academixs.com", "password": "123456"},
        {"username": "Kapil Savita", "email": "kapil.s@academixs.com", "password": "123456"},
    ]

    for data in users:
        db.add(User(**data))

    db.commit()
    print("✅ Users seeded successfully")
