from pydantic import BaseModel, Field
from typing import Optional, List

class Project(BaseModel):
    user_id: str
    title: str = Field(..., max_length=200)
    link: Optional[str] = Field(
        None, max_length=300,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    tech_stack: str = Field(..., max_length=200)
    date_range: Optional[str] = Field(None, max_length=50)
    description: List[str] = Field(default_factory=list)
