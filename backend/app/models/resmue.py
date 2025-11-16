from pydantic import BaseModel, Field
from typing import Optional

from .education import Education
from .work_exp import WorkExp
from .user import User


class Resmue(User):
    education: Optional[list[Education]] = None
    work_experience: Optional[list[WorkExp]] = None

    def _set_user_id(self, user_id: int):
        if self.work_experience:
            for we in self.work_experience:
                we.user_id = user_id
        if self.education:
            for edu in self.education:
                edu.user_id = user_id
