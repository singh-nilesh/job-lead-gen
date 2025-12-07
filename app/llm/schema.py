from typing import List, Optional
from pydantic import BaseModel, Field, validator
from app.db.mongo.types import Profile, Education, WorkExperience, ExtraCurricularActivity, Project, JobDescription
from datetime import datetime


# Schema for the structured resume output
class ResumeOutputSchema (BaseModel):
    profile: Profile
    education: Optional[List[Education]] = None
    work_experience: Optional[List[WorkExperience]] = None
    extra_curricular: Optional[List[ExtraCurricularActivity]] = None
    projects: Optional[List[Project]] = None


class CoverLetterOutputSchema (BaseModel):
    date: str = Field(..., default_factory=lambda: datetime.now().strftime("%B %d, %Y"))
    job_title: str
    company_name: Optional[str] = Field(default="Your Company")
    intro: str
    body_paragraphs: List[str] = Field(..., min_items=1, max_items=3)
    closing: str
    applicant_name: str
    phone: Optional[str] = None
    email: Optional[str] = None

    @validator("company_name", pre=True, always=True)
    def ensure_company_name(cls, v):
        return v or "your company"