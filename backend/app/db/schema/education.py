'''
DB table: education
    - Stores educational background information for users.
'''

from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.sqlalchemyConfig import Base


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    institution_name: Mapped[str] = mapped_column(String(200), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    field_of_study: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=True)
    grade: Mapped[str] = mapped_column(String(10), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # reference the Users
    user = relationship("Users", back_populates="user_edu")