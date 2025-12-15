from backend.domain.entities import (
    Area,
    Category,
    City,
    ContactEvent,
    LeadDelivery,
    LeadRequest,
    Plan,
    Provider,
    Review,
    Subscription,
    User,
)
from backend.infrastructure import models


def user_from_model(model: models.UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        password_hash=model.password_hash,
        phone=model.phone,
        phone_verified=model.phone_verified,
        created_at=model.created_at,
    )


def provider_from_model(model: models.ProviderModel) -> Provider:
    return Provider(
        id=model.id,
        user_id=model.user_id,
        name=model.name,
        bio_i18n=model.bio_i18n,
        avatar_url=model.avatar_url,
        verified=model.verified,
        languages=model.languages or [],
        categories=model.category_ids or [],
        city_id=model.city_id,
        area_ids=model.area_ids or [],
        pricing_hint=model.pricing_hint,
        availability=model.availability,
        whatsapp=model.whatsapp,
        phone=model.phone,
        rating=model.rating or 0.0,
        rating_count=model.rating_count or 0,
    )


def category_from_model(model: models.CategoryModel) -> Category:
    return Category(id=model.id, name_i18n=model.name_i18n)


def city_from_model(model: models.CityModel) -> City:
    return City(id=model.id, name_i18n=model.name_i18n)


def area_from_model(model: models.AreaModel) -> Area:
    return Area(id=model.id, city_id=model.city_id, name_i18n=model.name_i18n)


def lead_from_model(model: models.LeadRequestModel) -> LeadRequest:
    return LeadRequest(
        id=model.id,
        user_id=model.user_id,
        category_id=model.category_id,
        city_id=model.city_id,
        area_ids=model.area_ids or [],
        description=model.description,
        preferred_time=model.preferred_time,
        created_at=model.created_at,
    )


def delivery_from_model(model: models.LeadDeliveryModel) -> LeadDelivery:
    return LeadDelivery(
        id=model.id,
        lead_id=model.lead_id,
        provider_id=model.provider_id,
        status=model.status,
        created_at=model.created_at,
    )


def review_from_model(model: models.ReviewModel) -> Review:
    return Review(
        id=model.id,
        lead_delivery_id=model.lead_delivery_id,
        rating=model.rating,
        comment=model.comment,
        created_at=model.created_at,
    )


def plan_from_model(model: models.PlanModel) -> Plan:
    return Plan(
        id=model.id,
        name=model.name,
        plan_type=model.plan_type,
        monthly_credits=model.monthly_credits,
        price=model.price,
        features=model.features or [],
    )


def subscription_from_model(model: models.SubscriptionModel) -> Subscription:
    return Subscription(
        id=model.id,
        provider_id=model.provider_id,
        plan_id=model.plan_id,
        credits=model.credits,
        active=model.active,
        expires_at=model.expires_at,
    )


def contact_from_model(model: models.ContactEventModel) -> ContactEvent:
    return ContactEvent(
        id=model.id,
        provider_id=model.provider_id,
        user_id=model.user_id,
        lead_id=model.lead_id,
        token=model.token,
        created_at=model.created_at,
    )
