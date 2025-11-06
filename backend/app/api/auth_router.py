from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.db.sqlalchemyConfig import get_db
from app.services.auth import AuthService
from app.services.auth import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES

from app.services.auth import User
from app.models.users import Users as DbUser

# router init
router = APIRouter()


@router.post("/register")
def register_user(user: User, db: Session = Depends(get_db)):
    """ Register a new user """
    service = AuthService(db)
    if service._get_user_by_username(username=user.email):
        raise HTTPException(status_code=400, detail="Username already present")
    created: DbUser = service.create_user(new_user=user)
    return {"id": created.id, "username": created.email}


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Login user and return JWT token """
    service = AuthService(db)
    auth_user = service.authenticate_user(
        username= data.username,
        password= data.password
    )
    if not auth_user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth_user.email},
        expires_delta= access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
