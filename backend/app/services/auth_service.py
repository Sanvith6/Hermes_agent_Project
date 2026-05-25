from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate(self, username: str, password: str) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        return user

    async def register(self, username: str, email: str, password: str) -> User:
        # Check existing
        result = await self.db.execute(
            select(User).where((User.username == username) | (User.email == email))
        )
        if result.scalar_one_or_none():
            raise ValueError("User already exists")

        user = User(
            id=str(uuid4()),
            username=username,
            email=email,
            password_hash=get_password_hash(password)
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    def generate_tokens(self, user_id: str) -> dict:
        return {
            "access_token": create_access_token({"sub": user_id}),
            "refresh_token": create_refresh_token({"sub": user_id})
        }
