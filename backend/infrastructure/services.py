import json
import secrets
from datetime import datetime
from typing import Any, Dict

import httpx
from redis.asyncio import Redis

from backend.application import ports
from backend.infrastructure.config import get_settings


settings = get_settings()


def redis_client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)


class RedisOTPService(ports.OTPService):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def send(self, phone: str) -> None:
        code = f"{secrets.randbelow(999999):06d}"
        await self.redis.setex(f"otp:{phone}", 300, code)
        # In production integrate SMS gateway; here we just store code.

    async def verify(self, phone: str, code: str) -> bool:
        stored = await self.redis.get(f"otp:{phone}")
        return stored == code


class RedisRateLimiter(ports.RateLimiter):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_allowed(self, key: str, limit: int, ttl: int) -> bool:
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, ttl)
        return current <= limit


class ClickHouseAnalytics(ports.AnalyticsClient):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def track(self, event: str, payload: Dict[str, Any]) -> None:
        data = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload,
        }
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.base_url}/?query=INSERT INTO menna.events (event, timestamp, user_id, provider_id, city, category, metadata) VALUES",
                content=json.dumps(
                    [
                        [
                            data["event"],
                            data["timestamp"],
                            str(payload.get("user_id", "")),
                            str(payload.get("provider_id", "")),
                            str(payload.get("city_id", "")),
                            str(payload.get("category_id", "")),
                            payload,
                        ]
                    ]
                ),
                headers={"Content-Type": "application/json"},
            )
