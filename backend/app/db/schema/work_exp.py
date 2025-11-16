from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# package imports
from app.db.sqlalchemyConfig import Base


class WorkExp(Base):
    __tablename__ = "work_exp"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    source_url: Mapped[str] = mapped_column(String(200), nullable=True) 
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[str] = mapped_column(String(20), nullable=False)
    end_date: Mapped[str] = mapped_column(String(20), nullable=True)
    details: Mapped[str] = mapped_column(Text, nullable=True)

    # reference the Users
    user = relationship("Users", back_populates="user_work_exp")
