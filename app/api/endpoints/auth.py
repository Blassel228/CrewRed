from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import auth_service_dep, unit_of_work_dep
from app.schemas.auth import TokenResponse

router = APIRouter()


@router.post("/token/login", response_model=TokenResponse)
async def login(
    service: auth_service_dep,
    unit_of_work: unit_of_work_dep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await service.authenticate_user(
        unit_of_work=unit_of_work,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = service.create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token)
