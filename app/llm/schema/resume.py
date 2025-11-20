from typing import List, Optional
from pydantic import BaseModel, Field
from app.db.mongo.schema import Education, Work_experience, Profile

class ResumeInput(BaseModel):
    profile: Profile
    education: List[Education]
    work_experience: List[Work_experience]