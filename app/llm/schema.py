from typing import List, Optional
from pydantic import BaseModel, Field
from app.db.mongo.types import Profile, Education, WorkExperience, ExtraCurricularActivity, Project, JobDescription

# Schema for the structured resume output
class ResumeOutputSchema (BaseModel):
    profile: Profile
    education: Optional[List[Education]] = None
    work_experience: Optional[List[WorkExperience]] = None
    extra_curricular: Optional[List[ExtraCurricularActivity]] = None
    projects: Optional[List[Project]] = None

