from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core import settings
from app.db.models import User
from app.utils.unit_of_work import UnitOfWork

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

    async def authenticate_user(
        self, unit_of_work: UnitOfWork, email: str, password: str
    ) -> Optional[User]:
        async with unit_of_work:
            user = await unit_of_work.user.get_one_or_none({"email": email})

        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    async def login(self, unit_of_work: UnitOfWork, email: str, password: str) -> str:
        user = await self.authenticate_user(unit_of_work, email, password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return self.create_access_token({"sub": str(user.id), "email": user.email})

    async def get_current_user(
        self,
        token=Depends(oauth2_scheme),
        unit_of_work: UnitOfWork = Depends(UnitOfWork),
    ) -> User:
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
        async with unit_of_work:
            user = await unit_of_work.user.get_one_or_none({"id": UUID(user_id)})
        if user is None:
            raise credentials_exception

        return user


auth_service = AuthService()
