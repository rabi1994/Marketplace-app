from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from backend.domain.entities import (
    ContactEvent,
    LeadDelivery,
    LeadRequest,
    Review,
    User,
)
from backend.application import ports


@dataclass
class AuthResult:
    user: User
    access_token: str
    refresh_token: str


class RegisterUser:
    def __init__(self, users: ports.UserRepository, hasher: ports.PasswordHasher):
        self.users = users
        self.hasher = hasher

    async def execute(self, email: str, password: str, phone: Optional[str]) -> User:
        hashed = self.hasher.hash(password)
        user = User(id=None, email=email, password_hash=hashed, phone=phone, phone_verified=False)
        return await self.users.create(user)


class Login:
    def __init__(
        self,
        users: ports.UserRepository,
        hasher: ports.PasswordHasher,
        token_service: ports.TokenService,
        rate_limiter: ports.RateLimiter,
    ):
        self.users = users
        self.hasher = hasher
        self.token_service = token_service
        self.rate_limiter = rate_limiter

    async def execute(self, email: str, password: str) -> AuthResult:
        if not await self.rate_limiter.is_allowed(f"login:{email}", limit=5, ttl=300):
            raise ValueError("Too many attempts")
        user = await self.users.get_by_email(email)
        if not user or not self.hasher.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")
        return AuthResult(
            user=user,
            access_token=self.token_service.create_access_token(user.id),
            refresh_token=self.token_service.create_refresh_token(user.id),
        )


class RefreshToken:
    def __init__(self, token_service: ports.TokenService, users: ports.UserRepository):
        self.token_service = token_service
        self.users = users

    async def execute(self, refresh_token: str) -> AuthResult:
        user_id = self.token_service.verify_token(refresh_token)
        user = await self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        return AuthResult(
            user=user,
            access_token=self.token_service.create_access_token(user.id),
            refresh_token=self.token_service.create_refresh_token(user.id),
        )


class RequestOTP:
    def __init__(self, otp: ports.OTPService, limiter: ports.RateLimiter):
        self.otp = otp
        self.limiter = limiter

    async def execute(self, phone: str) -> None:
        if not await self.limiter.is_allowed(f"otp:{phone}", limit=3, ttl=300):
            raise ValueError("Too many OTP requests")
        await self.otp.send(phone)


class VerifyOTP:
    def __init__(self, otp: ports.OTPService, users: ports.UserRepository):
        self.otp = otp
        self.users = users

    async def execute(self, user_id: int, phone: str, code: str) -> bool:
        if not await self.otp.verify(phone, code):
            return False
        user = await self.users.get(user_id)
        if not user:
            return False
        user.phone = phone
        user.phone_verified = True
        await self.users.create(user)
        return True


class ResetPassword:
    def __init__(self, users: ports.UserRepository, hasher: ports.PasswordHasher):
        self.users = users
        self.hasher = hasher

    async def execute(self, email: str, new_password: str) -> bool:
        user = await self.users.get_by_email(email)
        if not user:
            return False
        user.password_hash = self.hasher.hash(new_password)
        await self.users.create(user)
        return True


class ListProviders:
    def __init__(self, providers: ports.ProviderRepository, analytics: ports.AnalyticsClient):
        self.providers = providers
        self.analytics = analytics

    async def execute(
        self,
        category_id: Optional[int] = None,
        city_id: Optional[int] = None,
        area_ids: Optional[List[int]] = None,
        verified: Optional[bool] = None,
        language: Optional[str] = None,
        sort: Optional[str] = None,
    ):
        providers = await self.providers.list(
            category_id=category_id,
            city_id=city_id,
            area_ids=area_ids,
            verified=verified,
            language=language,
            sort=sort,
        )
        await self.analytics.track(
            "provider_profile_viewed",
            {"category_id": category_id, "city_id": city_id, "count": len(providers)},
        )
        return providers


class GetProviderProfile:
    def __init__(self, providers: ports.ProviderRepository, analytics: ports.AnalyticsClient):
        self.providers = providers
        self.analytics = analytics

    async def execute(self, provider_id: int):
        provider = await self.providers.get(provider_id)
        if provider:
            await self.analytics.track("provider_profile_viewed", {"provider_id": provider_id})
        return provider


class CreateLeadRequest:
    def __init__(
        self,
        leads: ports.LeadRepository,
        providers: ports.ProviderRepository,
        analytics: ports.AnalyticsClient,
    ):
        self.leads = leads
        self.providers = providers
        self.analytics = analytics

    async def execute(
        self,
        user_id: int,
        category_id: int,
        city_id: int,
        area_ids: List[int],
        description: str,
        preferred_time: Optional[str],
    ) -> LeadRequest:
        lead = LeadRequest(
            id=None,
            user_id=user_id,
            category_id=category_id,
            city_id=city_id,
            area_ids=area_ids,
            description=description,
            preferred_time=preferred_time,
        )
        lead = await self.leads.create(lead)
        await self.analytics.track(
            "lead_created",
            {"lead_id": lead.id, "city_id": city_id, "category_id": category_id},
        )
        return lead


class DeliverLead:
    def __init__(
        self,
        leads: ports.LeadRepository,
        analytics: ports.AnalyticsClient,
        subscriptions: ports.SubscriptionRepository,
    ):
        self.leads = leads
        self.analytics = analytics
        self.subscriptions = subscriptions

    async def execute(self, lead_id: int, provider_id: int) -> LeadDelivery:
        subscription = await self.subscriptions.get_active(provider_id)
        if subscription and subscription.credits > 0:
            await self.subscriptions.decrement_credit(subscription.id)
        delivery = LeadDelivery(
            id=None, lead_id=lead_id, provider_id=provider_id, status="delivered"
        )
        delivery = await self.leads.add_delivery(delivery)
        await self.analytics.track(
            "lead_delivered",
            {"lead_id": lead_id, "provider_id": provider_id},
        )
        return delivery


class CreateContactToken:
    def __init__(
        self,
        contacts: ports.ContactRepository,
        analytics: ports.AnalyticsClient,
    ):
        self.contacts = contacts
        self.analytics = analytics

    async def execute(self, provider_id: int, user_id: int, lead_id: Optional[int]) -> str:
        import secrets

        token = secrets.token_urlsafe(16)
        await self.contacts.create(
            ContactEvent(
                id=None,
                provider_id=provider_id,
                user_id=user_id,
                lead_id=lead_id,
                token=token,
            )
        )
        await self.analytics.track(
            "provider_contact_clicked",
            {"provider_id": provider_id, "user_id": user_id, "lead_id": lead_id},
        )
        return token


class CreateReview:
    def __init__(
        self,
        leads: ports.LeadRepository,
        reviews: ports.ReviewRepository,
        providers: ports.ProviderRepository,
        analytics: ports.AnalyticsClient,
    ):
        self.leads = leads
        self.reviews = reviews
        self.providers = providers
        self.analytics = analytics

    async def execute(
        self, lead_id: int, provider_id: int, user_id: int, rating: int, comment: Optional[str]
    ) -> Review:
        if not await self.leads.has_contact(lead_id, provider_id, user_id):
            raise ValueError("No valid contact")
        review = Review(
            id=None,
            lead_delivery_id=lead_id,
            rating=rating,
            comment=comment,
        )
        review = await self.reviews.create(review)
        await self.analytics.track(
            "review_created",
            {"provider_id": provider_id, "lead_id": lead_id, "rating": rating},
        )
        provider = await self.providers.get(provider_id)
        if provider:
            total = provider.rating * provider.rating_count + rating
            count = provider.rating_count + 1
            await self.providers.update_rating(provider_id, total / count, count)
        return review
