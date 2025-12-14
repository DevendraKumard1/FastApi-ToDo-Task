# Todo Task Project

A simple Todo Task project.

## Table of Contents

- [Installation](#installation)

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/DevendraKumard1/FastApi-ToDo-Task.git
cd your-fastapi-project

2. **Create Vurtual Environment**:
python -m venv venv
source venv/bin/activate

3. **Install Dependencies**:
pip install -r requirements.txt

4. **Run Server**:
uvicorn main:app --reload
or
uvicorn index:app --reload

5. **Open in Browser**:
http://127.0.0.1:8000/docs

6. **Seed run via command**:
python -m app.seed

7. **Migration via command**:
# alembic revision --autogenerate -m "initial"
# or
# alembic revision --autogenerate -m "create users and todos table"
# or
# alembic upgrade head

8. **Migration railway via command**:
# Run migration and seeder on Production

railway login
railway link  
railway run alembic upgrade head
railway run python -m alembic upgrade head
railway run python -m app.seed

# Connect railway database on terminal
mysql -u root -p -h hopper.proxy.rlwy.net -P 23795
