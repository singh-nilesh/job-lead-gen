from pydantic import BaseModel, Field
from typing import Optional


class ExtraCurricularActivity(BaseModel):
    user_id: str
    activity: str
    organization: Optional[str] = None
    description: list[str] = Field(default_factory=list)