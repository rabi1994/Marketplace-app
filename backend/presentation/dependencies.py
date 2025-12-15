from redis.asyncio import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infrastructure.config import get_settings
from backend.infrastructure.db import get_session
from backend.infrastructure.repositories import (
    SqlAlchemyContactRepository,
    SqlAlchemyGeographyRepository,
    SqlAlchemyLeadRepository,
    SqlAlchemyPlanRepository,
    SqlAlchemyProviderRepository,
    SqlAlchemyReviewRepository,
    SqlAlchemySubscriptionRepository,
    SqlAlchemyUserRepository,
)
from backend.infrastructure.security import Argon2PasswordHasher, JWTTokenService
from backend.infrastructure.services import ClickHouseAnalytics, RedisOTPService, RedisRateLimiter, redis_client


def get_db_session() -> AsyncSession:
    return Depends(get_session)  # type: ignore


async def get_repositories(session: AsyncSession = Depends(get_session)):
    return {
        "users": SqlAlchemyUserRepository(session),
        "providers": SqlAlchemyProviderRepository(session),
        "geography": SqlAlchemyGeographyRepository(session),
        "leads": SqlAlchemyLeadRepository(session),
        "reviews": SqlAlchemyReviewRepository(session),
        "plans": SqlAlchemyPlanRepository(session),
        "subscriptions": SqlAlchemySubscriptionRepository(session),
        "contacts": SqlAlchemyContactRepository(session),
    }


async def get_services():
    settings = get_settings()
    redis: Redis = redis_client()
    return {
        "otp": RedisOTPService(redis),
        "limiter": RedisRateLimiter(redis),
        "token": JWTTokenService(),
        "analytics": ClickHouseAnalytics(settings.clickhouse_url),
        "hasher": Argon2PasswordHasher(),
    }
