import pytest
from backend.application.use_cases import Login, RegisterUser
from backend.application import ports
from backend.domain.entities import User


class InMemoryUserRepo(ports.UserRepository):
    def __init__(self):
        self.users = {}
        self._id = 1

    async def create(self, user: User) -> User:
        if not user.id:
            user.id = self._id
            self._id += 1
        self.users[user.email] = user
        return user

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def get(self, user_id: int):
        for u in self.users.values():
            if u.id == user_id:
                return u
        return None


class DummyHasher(ports.PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed-{password}"

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed-{plain_password}"


class DummyToken(ports.TokenService):
    def create_access_token(self, user_id: int) -> str:
        return "access"

    def create_refresh_token(self, user_id: int) -> str:
        return "refresh"

    def verify_token(self, token: str) -> int:
        return 1


class DummyLimiter(ports.RateLimiter):
    async def is_allowed(self, key: str, limit: int, ttl: int) -> bool:
        return True


def test_register_and_login_flow():
    import asyncio

    async def run():
        repo = InMemoryUserRepo()
        hasher = DummyHasher()
        register = RegisterUser(repo, hasher)
        user = await register.execute("a@test.com", "secret", None)
        assert user.id == 1

        login = Login(repo, hasher, DummyToken(), DummyLimiter())
        result = await login.execute("a@test.com", "secret")
        assert result.access_token == "access"

    asyncio.run(run())
