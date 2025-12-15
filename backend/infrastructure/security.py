from datetime import datetime, timedelta
from jose import jwt
from passlib.hash import argon2

from backend.application import ports
from backend.infrastructure.config import get_settings

settings = get_settings()


class JWTTokenService(ports.TokenService):
    def create_access_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        return jwt.encode({"sub": str(user_id), "exp": expire}, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        return jwt.encode({"sub": str(user_id), "exp": expire}, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def verify_token(self, token: str) -> int:
        data = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return int(data["sub"])


class Argon2PasswordHasher(ports.PasswordHasher):
    def hash(self, password: str) -> str:
        return argon2.using(
            time_cost=settings.argon2_time_cost,
            memory_cost=settings.argon2_memory_cost,
            parallelism=settings.argon2_parallelism,
        ).hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return argon2.verify(plain_password, hashed_password)
