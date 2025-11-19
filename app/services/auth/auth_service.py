from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .user import User
from app.db import schema
from app.core.logger import service_logger as logger


# Switching to sha256_crypt, becaues facing dependency issues with bcrypt and python 13
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

class AuthService:
    """ Service wrapping for common user's auth opertaions.

    Usage:
        service = AuthService(db_session)
        service.create_user(username, password)
        service.authenticate_user(username, password)
    """

    def __init__(self, db:Session):
        self.db = db
    
    
    def create_user(self, new_user:User):
        """ Create a new user in the database """
        logger.info(f"Creating new user: {new_user.email}")
        
        pwd_hash = pwd_context.hash(new_user.password)
        user = schema.Users(**new_user.model_dump())
        
        # Override password with hashed password, and set is_active to True
        user.password = pwd_hash
        user.is_active = True

        logger.info(f"Storing new user in database, user:{new_user.email}")
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"New user created successfully: {user.email}, id={user.id}")
            return user
        
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user: {new_user.email}, error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while creating user: {new_user.email}, error: {e}")        


    def _get_user_by_username(self, username:str):
        """ Get user by username (email) """
        try:
            logger.info(f"Fetching user by username: {username}")
            user = self.db.query(schema.Users).filter(schema.Users.email == username).first()
            if user:
                logger.info(f"User found: {username} (id={user.id})")
            else:
                logger.info(f"User not found: {username}")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching user: {username}, error: {e}")


    def authenticate_user(self, username:str, password:str):
        """ Authenticate user by username and password (login) """
        logger.info(f"Authenticating user: {username}")
        auth_user:schema.Users  = self._get_user_by_username(username)

        if auth_user and pwd_context.verify(password, auth_user.password):
            logger.info(f"User authenticated successfully: {username}")
            return auth_user
        else:
            logger.warning(f"Authentication failed for user: {username}")
            return None