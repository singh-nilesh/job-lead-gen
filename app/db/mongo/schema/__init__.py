''' Always export collection names in snake_case
- Standardized naming for MongoDB collections
'''
from .education import Education as education
from .work_experience import WorkExperience as work_experience
from .profile import Profile as profile
from .extra_curricular import ExtraCurricularActivity as extra_curricular
from .projects import Project as projects
from .job_description import JobDescription as job_description

__all__ = [
    "education",
    "work_experience",
    "profile",
    "extra_curricular",
    "projects",
    "job_description",
]