from sqlalchemy.orm import Session
from app.services.auth_service import authenticate_user, create_access_token

class UserService:
    def user_login(self, db: Session, username: str, password: str):
        user_record = authenticate_user(db, username, password)
    
        if not user_record.get("success"):
            return {
                "success": False,
                "message": user_record["message"]
            }
        
        access_token = create_access_token(data={"sub": username})
        
        return {
            "success": True,
            'result': user_record["data"],
            "access_token": access_token, 
        }