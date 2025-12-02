from pydantic import BaseModel, Field
from typing import Optional

class Profile(BaseModel):
    user_id: str
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=100)
    location: str = Field(..., min_length=2, max_length=70)
    phone: str = Field(
        ...,
        pattern=r'^\+91\s?[6-9]\d{9}$',
        description="Phone number must be entered in the format: '+91 9900114011' or '+919900114011'"
    )
    website: Optional[str] = Field(
        None,
        max_length=200,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    github: Optional[str] = Field(
        None,
        max_length=200,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    linkedin: Optional[str] = Field(
        None,
        max_length=200,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    professional_summary: str = Field(None, max_length=1000)

    skills: list[str] = Field(default=None,
                              description= '''
                                List of skills, domain: details, eg.
                                Cloud & DevOps: Docker Compose, Kubernetes, AWS, GitHub Actions
                                Programming Languages: Python, JavaScript, TypeScript
                                '''
                              )
    certifications: Optional[list[str]] = Field(default=None, description="List of certifications")
    
