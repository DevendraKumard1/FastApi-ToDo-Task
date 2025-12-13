from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes import router

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost:3000",
    "https://dev-todo-task.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from routes.py
app.include_router(router)