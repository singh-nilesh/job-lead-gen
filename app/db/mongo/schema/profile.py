from pydantic import BaseModel, Field
from typing import Optional

class Profile(BaseModel):
    user_id: str
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=100)
    location: str = Field(..., min_length=2, max_length=70)
    phone: str = Field(
        ...,
        pattern=r'^\+91\s?[0-9]\d{10}$',
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
    designation: Optional[list[str]] = Field(None, max_length=50)
    professional_summary: Optional[str] = Field(None, max_length=500)

    skills: list[str] = Field(None, max_length=150,
                              description= '''
                                List of skills, domain: details, eg.
                                Cloud & DevOps: Docker Compose, Kubernetes, AWS, GitHub Actions
                                Programming Languages: Python, JavaScript, TypeScript
                                '''
                              )
    certifications: Optional[list[str]] = Field(None, max_length=150)
    
