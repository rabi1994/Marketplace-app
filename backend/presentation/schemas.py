from typing import List, Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    phone: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProviderResponse(BaseModel):
    id: int
    name: str
    bio_i18n: dict
    avatar_url: Optional[str]
    verified: bool
    languages: List[str]
    categories: List[int]
    city_id: int
    area_ids: List[int]
    pricing_hint: Optional[str]
    availability: Optional[str]
    whatsapp: Optional[str]
    phone: Optional[str]
    rating: float
    rating_count: int

    class Config:
        orm_mode = True


class LeadRequestPayload(BaseModel):
    category_id: int
    city_id: int
    area_ids: List[int]
    description: str
    preferred_time: Optional[str]


class ReviewPayload(BaseModel):
    lead_id: int
    provider_id: int
    rating: int
    comment: Optional[str] = None
