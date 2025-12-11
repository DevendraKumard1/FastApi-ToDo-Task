from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.services.user_service import UserService
from fastapi.security import OAuth2PasswordRequestForm

class AuthController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    # ------------------------------
    # User Login functionality
    # ------------------------------
    def login(self, db: Session, form_data: OAuth2PasswordRequestForm):
        try:
            user = self.user_service.user_login(db, form_data.username, form_data.password)
            
            if not user.get("success"):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=user["message"],
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {
                "status": status.HTTP_200_OK,
                "result": user["result"],
                "access_token": user["access_token"],
                "token_type": "bearer",
                "message": "User logged in successfully",
            }
        except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error creating todo: {e}")
