
from pydantic import BaseModel, Field
from typing import Optional


class JobDescription(BaseModel):
    user_id: str
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    description: list[str] = Field(..., description="Full job description text")
    skills: list[str] = Field(None, description="List of required skills")
    url: Optional[str] = Field(None, description="URL to the job posting")
    application_date: Optional[str] = Field(None, description="Date of application submission")
