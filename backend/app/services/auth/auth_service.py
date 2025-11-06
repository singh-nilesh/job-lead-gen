from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User
from app.models.users import Users as DbUsers
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
        user = DbUsers(**new_user.model_dump())
        user.password = pwd_hash

        logger.info(f"Storing new user in database, user:{new_user.email}")
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"New user created successfully: {user.email}")
            return user
        except Exception as e:
            logger.exception(f"Failed to create new user, error: {e}")
            return None
        

    def _get_user_by_username(self, username:str):
        """ Get user by username (email) """
        return self.db.query(DbUsers).filter(DbUsers.email == username).first()
    

    def authenticate_user(self, username:str, password:str):
        """ Authenticate user by username and password (login) """
        auth_user:DbUsers  = self._get_user_by_username(username)
        if not auth_user:
            return False
        if not pwd_context.verify(password, auth_user.password):
            return False
        return auth_user