from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

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


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        ...


class ProviderRepository(ABC):
    @abstractmethod
    async def list(
        self,
        category_id: Optional[int] = None,
        city_id: Optional[int] = None,
        area_ids: Optional[List[int]] = None,
        verified: Optional[bool] = None,
        language: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> List[Provider]:
        ...

    @abstractmethod
    async def get(self, provider_id: int) -> Optional[Provider]:
        ...

    @abstractmethod
    async def update_rating(self, provider_id: int, rating: float, count: int) -> None:
        ...


class GeographyRepository(ABC):
    @abstractmethod
    async def list_cities(self) -> List[City]:
        ...

    @abstractmethod
    async def list_areas(self, city_id: int) -> List[Area]:
        ...

    @abstractmethod
    async def list_categories(self) -> List[Category]:
        ...


class LeadRepository(ABC):
    @abstractmethod
    async def create(self, lead: LeadRequest) -> LeadRequest:
        ...

    @abstractmethod
    async def add_delivery(self, delivery: LeadDelivery) -> LeadDelivery:
        ...

    @abstractmethod
    async def update_delivery_status(self, delivery_id: int, status: str) -> None:
        ...

    @abstractmethod
    async def has_contact(self, lead_id: int, provider_id: int, user_id: int) -> bool:
        ...


class ReviewRepository(ABC):
    @abstractmethod
    async def create(self, review: Review) -> Review:
        ...


class SubscriptionRepository(ABC):
    @abstractmethod
    async def get_active(self, provider_id: int) -> Optional[Subscription]:
        ...

    @abstractmethod
    async def decrement_credit(self, subscription_id: int) -> None:
        ...


class PlanRepository(ABC):
    @abstractmethod
    async def list(self) -> List[Plan]:
        ...


class ContactRepository(ABC):
    @abstractmethod
    async def create(self, event: ContactEvent) -> ContactEvent:
        ...


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: int) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str:
        ...

    @abstractmethod
    def verify_token(self, token: str) -> int:
        ...


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        ...


class OTPService(ABC):
    @abstractmethod
    async def send(self, phone: str) -> None:
        ...

    @abstractmethod
    async def verify(self, phone: str, code: str) -> bool:
        ...


class RateLimiter(ABC):
    @abstractmethod
    async def is_allowed(self, key: str, limit: int, ttl: int) -> bool:
        ...


class AnalyticsClient(ABC):
    @abstractmethod
    async def track(self, event: str, payload: dict) -> None:
        ...
