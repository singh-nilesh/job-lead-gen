from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(
        ...,
        pattern=r'^\+?1?\d{15}$',
        description="Phone number must be entered in the format: '+999999999' "
    )
    location: str = Field(..., min_length=2, max_length=70)
    password: str = Field(..., min_length=8, max_length=50)

