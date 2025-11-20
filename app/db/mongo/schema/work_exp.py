from pydantic import BaseModel, Field
from typing import Optional

class WorkExp(BaseModel):
    user_id: int
    title: str = Field(..., max_length=200)
    source_url: Optional[str] = Field(
        None,
        max_length=200,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        )
    company_name: str = Field(..., max_length=200)
    location: str = Field(..., max_length=100)
    start_date: str = Field(..., max_length=20)
    end_date: Optional[str] = Field(None, max_length=20)
    details: Optional[str] = None