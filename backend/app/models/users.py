from sqlalchemy import Column, Integer, String
from app.db.sqlalchemyConfig import Base

# Users table for Auth
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True ,nullable=False)
    phone = Column(String(10), nullable=False)
    location = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
