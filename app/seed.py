# seed.py
from app.database import SessionLocal
from app.seeders.user_seeder import seed_users

def run_seeders():
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()
