from pydantic import BaseModel, Field
from typing import Optional, List

class WorkExperience(BaseModel):
    user_id: str
    title: str = Field(..., max_length=200)
    link: Optional[str] = Field(
        None, max_length=300,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    company_name: str = Field(..., max_length=200)
    location: str = Field(..., max_length=100)
    date_range: str = Field(..., max_length=50)
    description: List[str] = Field(default_factory=list)
