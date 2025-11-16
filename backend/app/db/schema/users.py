''''
DB Table: Users
    - table to store user information for authentication and profile details
    - partent table for WorkExp, achievements and Education tables
    - has cascade delete on related records
'''

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.sqlalchemyConfig import Base

# Users table for Auth
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(17), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str] = mapped_column(String(255), nullable=True)


    # add bidirectional relationship
    user_work_exp = relationship("WorkExp", back_populates="user", cascade="all, delete-orphan")
    user_edu = relationship("Education", back_populates="user", cascade="all, delete-orphan")
