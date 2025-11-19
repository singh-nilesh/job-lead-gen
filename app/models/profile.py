from pydantic import BaseModel, Field
from typing import Optional

class Profile(BaseModel):
    user_id: int
    email: str = Field(..., max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    designation: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(
        None,
        max_length=200,
        pattern=r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    )
    phone: str = Field(
        ...,
        pattern=r'^\+91\s?[6-9]\d{9}$',
        description="Phone number must be entered in the format: '+91 9900114011' or '+919900114011'"
    )
    location: str = Field(..., min_length=2, max_length=70)