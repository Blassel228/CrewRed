from datetime import datetime, timedelta, timezone
from uuid import UUID
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends

from app.core import settings
from app.db.models import User
from app.repositories.user import UserRepository
from app.utils.deps import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token/login")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def login(
        self, db: AsyncSession, email: str, password: str, repo: UserRepository
    ) -> str:
        user = await self.authenticate_user(db, repo, email, password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self.create_access_token({"sub": str(user.id), "email": user.email})

    async def authenticate_user(
        self, db: AsyncSession, repo: UserRepository, email: str, password: str
    ):
        user = await repo.get_one_or_none(db, {"email": email})
        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    async def get_current_user(
        self,
        token=Depends(oauth2_scheme),
        db=Depends(get_db),
        repo=Depends(UserRepository),
    ) -> Sequence[User]:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await repo.get_one_or_none(db, {"id": UUID(user_id)})
        if user is None:
            raise credentials_exception
        return user


auth_service = AuthService()
