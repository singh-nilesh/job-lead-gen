from pydantic import BaseModel, Field
from typing import Optional

class Education(BaseModel):
    user_id: int
    institution_name: str = Field(..., max_length=200)
    degree: str = Field(..., max_length=100)
    field_of_study: str = Field(..., max_length=100)
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    grade: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = None

