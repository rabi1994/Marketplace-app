from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Text,
    Enum,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from backend.domain.entities import LeadStatus, PlanType
from backend.infrastructure.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    phone_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("ProviderModel", back_populates="user", uselist=False)


class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name_i18n = Column(JSONB, nullable=False)


class CityModel(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True)
    name_i18n = Column(JSONB, nullable=False)


class AreaModel(Base):
    __tablename__ = "areas"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    name_i18n = Column(JSONB, nullable=False)

    city = relationship("CityModel")


class ProviderModel(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    bio_i18n = Column(JSONB, nullable=False)
    avatar_url = Column(String)
    verified = Column(Boolean, default=False)
    languages = Column(ARRAY(String))
    category_ids = Column(ARRAY(Integer))
    city_id = Column(Integer, ForeignKey("cities.id"))
    area_ids = Column(ARRAY(Integer))
    pricing_hint = Column(String)
    availability = Column(String)
    whatsapp = Column(String)
    phone = Column(String)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)

    user = relationship("UserModel", back_populates="provider")
    city = relationship("CityModel")


class LeadRequestModel(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    area_ids = Column(ARRAY(Integer))
    description = Column(Text)
    preferred_time = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class LeadDeliveryModel(Base):
    __tablename__ = "lead_deliveries"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    status = Column(Enum(LeadStatus), default=LeadStatus.DELIVERED)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReviewModel(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    lead_delivery_id = Column(Integer, ForeignKey("lead_deliveries.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class PlanModel(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    plan_type = Column(Enum(PlanType))
    monthly_credits = Column(Integer)
    price = Column(Float)
    features = Column(ARRAY(String))


class SubscriptionModel(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    credits = Column(Integer)
    active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)


class ContactEventModel(Base):
    __tablename__ = "contact_events"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    token = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
