from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.core.logger import service_logger as logger
from fastapi import HTTPException, status
from typing import Optional
from app.core.config import Settings

# Import environment variables
SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Method to create a new access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # use numeric timestamp for "exp"
    to_encode.update({"exp": int(expire.timestamp())})
    logger.info(f"Creating access token for {data.get('sub')} expiring at {expire.isoformat()}")

    try:
        encode_jwt = jwt.encode(
            to_encode,
            key= SECRET_KEY,
            algorithm= ALGORITHM
        )
    except Exception as e:
        logger.error("Error creating access token: %s", e)
        return None
    return encode_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")
        if username is None:
            logger.warning("Token is invalid or expired")
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        logger.warning("Token is invalid or expired")
        raise HTTPException(status_code=403, detail="Token is invalid or expired")