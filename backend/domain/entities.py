from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


LocaleMap = Dict[str, str]


class PlanType(str, Enum):
    PAY_PER_LEAD = "pay_per_lead"
    SUBSCRIPTION = "subscription"


class LeadStatus(str, Enum):
    NEW = "new"
    DELIVERED = "delivered"
    OPENED = "opened"
    RESPONDED = "responded"


@dataclass
class User:
    id: Optional[int]
    email: str
    password_hash: str
    phone: Optional[str]
    phone_verified: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Category:
    id: Optional[int]
    name_i18n: LocaleMap


@dataclass
class City:
    id: Optional[int]
    name_i18n: LocaleMap


@dataclass
class Area:
    id: Optional[int]
    city_id: int
    name_i18n: LocaleMap


@dataclass
class Provider:
    id: Optional[int]
    user_id: int
    name: str
    bio_i18n: LocaleMap
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
    rating: float = 0.0
    rating_count: int = 0


@dataclass
class LeadRequest:
    id: Optional[int]
    user_id: int
    category_id: int
    city_id: int
    area_ids: List[int]
    description: str
    preferred_time: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LeadDelivery:
    id: Optional[int]
    lead_id: int
    provider_id: int
    status: LeadStatus
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Review:
    id: Optional[int]
    lead_delivery_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Plan:
    id: Optional[int]
    name: str
    plan_type: PlanType
    monthly_credits: int
    price: float
    features: List[str] = field(default_factory=list)


@dataclass
class Subscription:
    id: Optional[int]
    provider_id: int
    plan_id: int
    credits: int
    active: bool
    expires_at: Optional[datetime]


@dataclass
class ContactEvent:
    id: Optional[int]
    provider_id: int
    user_id: int
    lead_id: Optional[int]
    token: str
    created_at: datetime = field(default_factory=datetime.utcnow)
