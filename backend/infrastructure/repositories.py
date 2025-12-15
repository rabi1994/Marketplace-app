from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application import ports
from backend.domain.entities import ContactEvent, LeadDelivery, LeadRequest, Provider, Review, Subscription, User
from backend.infrastructure import models, mappers


class SqlAlchemyUserRepository(ports.UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        if user.id:
            stmt = (
                update(models.UserModel)
                .where(models.UserModel.id == user.id)
                .values(
                    phone=user.phone,
                    phone_verified=user.phone_verified,
                    password_hash=user.password_hash,
                )
                .returning(models.UserModel)
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one()
        else:
            model = models.UserModel(
                email=user.email,
                password_hash=user.password_hash,
                phone=user.phone,
                phone_verified=user.phone_verified,
            )
            self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return mappers.user_from_model(model)

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(models.UserModel).where(models.UserModel.email == email))
        model = result.scalar_one_or_none()
        return mappers.user_from_model(model) if model else None

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(models.UserModel).where(models.UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return mappers.user_from_model(model) if model else None


class SqlAlchemyProviderRepository(ports.ProviderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(
        self,
        category_id: Optional[int] = None,
        city_id: Optional[int] = None,
        area_ids: Optional[List[int]] = None,
        verified: Optional[bool] = None,
        language: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Provider]:
        query = select(models.ProviderModel)
        if category_id:
            query = query.where(models.ProviderModel.category_ids.any(category_id))
        if city_id:
            query = query.where(models.ProviderModel.city_id == city_id)
        if area_ids:
            for area in area_ids:
                query = query.where(models.ProviderModel.area_ids.any(area))
        if verified is not None:
            query = query.where(models.ProviderModel.verified == verified)
        if language:
            query = query.where(models.ProviderModel.languages.any(language))
        if sort == "rating":
            query = query.order_by(models.ProviderModel.rating.desc())
        result = await self.session.execute(query)
        return [mappers.provider_from_model(row) for row in result.scalars().all()]

    async def get(self, provider_id: int) -> Optional[Provider]:
        result = await self.session.execute(select(models.ProviderModel).where(models.ProviderModel.id == provider_id))
        model = result.scalar_one_or_none()
        return mappers.provider_from_model(model) if model else None

    async def update_rating(self, provider_id: int, rating: float, count: int) -> None:
        await self.session.execute(
            update(models.ProviderModel)
            .where(models.ProviderModel.id == provider_id)
            .values(rating=rating, rating_count=count)
        )
        await self.session.commit()


class SqlAlchemyGeographyRepository(ports.GeographyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_cities(self):
        res = await self.session.execute(select(models.CityModel))
        return [mappers.city_from_model(m) for m in res.scalars().all()]

    async def list_areas(self, city_id: int):
        res = await self.session.execute(select(models.AreaModel).where(models.AreaModel.city_id == city_id))
        return [mappers.area_from_model(m) for m in res.scalars().all()]

    async def list_categories(self):
        res = await self.session.execute(select(models.CategoryModel))
        return [mappers.category_from_model(m) for m in res.scalars().all()]


class SqlAlchemyLeadRepository(ports.LeadRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, lead: LeadRequest) -> LeadRequest:
        model = models.LeadRequestModel(
            user_id=lead.user_id,
            category_id=lead.category_id,
            city_id=lead.city_id,
            area_ids=lead.area_ids,
            description=lead.description,
            preferred_time=lead.preferred_time,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return mappers.lead_from_model(model)

    async def add_delivery(self, delivery: LeadDelivery) -> LeadDelivery:
        model = models.LeadDeliveryModel(
            lead_id=delivery.lead_id, provider_id=delivery.provider_id, status=delivery.status
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return mappers.delivery_from_model(model)

    async def update_delivery_status(self, delivery_id: int, status: str) -> None:
        await self.session.execute(
            update(models.LeadDeliveryModel).where(models.LeadDeliveryModel.id == delivery_id).values(status=status)
        )
        await self.session.commit()

    async def has_contact(self, lead_id: int, provider_id: int, user_id: int) -> bool:
        q = select(models.ContactEventModel).where(
            models.ContactEventModel.lead_id == lead_id,
            models.ContactEventModel.provider_id == provider_id,
            models.ContactEventModel.user_id == user_id,
        )
        res = await self.session.execute(q)
        return res.scalar_one_or_none() is not None


class SqlAlchemyReviewRepository(ports.ReviewRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, review: Review) -> Review:
        model = models.ReviewModel(
            lead_delivery_id=review.lead_delivery_id, rating=review.rating, comment=review.comment
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return mappers.review_from_model(model)


class SqlAlchemySubscriptionRepository(ports.SubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active(self, provider_id: int) -> Optional[Subscription]:
        res = await self.session.execute(
            select(models.SubscriptionModel).where(
                models.SubscriptionModel.provider_id == provider_id, models.SubscriptionModel.active.is_(True)
            )
        )
        model = res.scalar_one_or_none()
        return mappers.subscription_from_model(model) if model else None

    async def decrement_credit(self, subscription_id: int) -> None:
        await self.session.execute(
            update(models.SubscriptionModel)
            .where(models.SubscriptionModel.id == subscription_id)
            .values(credits=models.SubscriptionModel.credits - 1)
        )
        await self.session.commit()


class SqlAlchemyPlanRepository(ports.PlanRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self):
        res = await self.session.execute(select(models.PlanModel))
        return [mappers.plan_from_model(m) for m in res.scalars().all()]


class SqlAlchemyContactRepository(ports.ContactRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: ContactEvent) -> ContactEvent:
        model = models.ContactEventModel(
            provider_id=event.provider_id,
            user_id=event.user_id,
            lead_id=event.lead_id,
            token=event.token,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return mappers.contact_from_model(model)
