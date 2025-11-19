from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta

from app.db.sqlalchemyConfig import get_auth_db
from app.services.auth import AuthService
from app.services.auth import User

from app.core.logger import api_logger as logger
from app.services.auth import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES


# router init
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
def register_user(user: User, db: Session = Depends(get_auth_db)):
    """ Register a new user """
    logger.info(f"Register attempt for user: {user.email}")

    # check existing user
    service = AuthService(db)
    if service._get_user_by_username(username=user.email):
        logger.warning(f"Registration failed - username already present: {user.email}")
        raise HTTPException(status_code=400, detail="Username already present")
    
    # If user not present, create new user
    created = service.create_user(new_user=user)
    if created:
        logger.info(f"User registered successfully: {created.email} (id={created.id})")
        return {"id": created.id, "username": created.email}
    else:
        logger.error(f"User registration failed for: {user.email}")
        raise HTTPException(status_code=500, detail="User registration failed")


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_auth_db)):
    """ Login user and return JWT token """
    logger.info("Login attempt for user: %s", data.username)
    
    service = AuthService(db)
    auth_user = service.authenticate_user(
        username= data.username,
        password= data.password
    )
    # If authentication fails
    if not auth_user:
        logger.warning("Authentication failed for user: %s", data.username)
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Create JWT token, on successful authentication
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth_user.email},
        expires_delta= access_token_expires
    )
    if not access_token:
        logger.error("Failed to create access token for user: %s", data.username)
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )
    logger.info("User authenticated: %s — access token issued (expires in %s minutes)", auth_user.email, ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": auth_user.id,
            "email": auth_user.email
        }
    }


# verify-token endpoint
@router.get("/verify-token/{token}")
def verify_jwt_token(token: str):
    """ Verify JWT token validity """
    logger.info("Token verification attempt")
    token_payload = verify_token(token)

    if token_payload:
        logger.info("Token is valid for user", token_payload.get("sub"))
        return {
            "valid": True,
            "user": token_payload.get("sub"),
            "expires_at": token_payload.get("exp")
        }
    else:
        logger.warning("Token is invalid")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )