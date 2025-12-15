from typing import Optional
from fastapi import APIRouter, Depends, HTTPException

from backend.application.use_cases import (
    CreateContactToken,
    CreateLeadRequest,
    CreateReview,
    DeliverLead,
    GetProviderProfile,
    ListProviders,
    Login,
    RefreshToken,
    RegisterUser,
    RequestOTP,
    ResetPassword,
    VerifyOTP,
)
from backend.presentation import schemas
from backend.presentation.dependencies import get_repositories, get_services

router = APIRouter()


@router.post("/auth/register", response_model=schemas.TokenResponse)
async def register(payload: schemas.RegisterRequest, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = RegisterUser(repos["users"], services["hasher"])
    user = await uc.execute(payload.email, payload.password, payload.phone)
    token_service = services["token"]
    return schemas.TokenResponse(
        access_token=token_service.create_access_token(user.id),
        refresh_token=token_service.create_refresh_token(user.id),
    )


@router.post("/auth/login", response_model=schemas.TokenResponse)
async def login(payload: schemas.LoginRequest, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = Login(repos["users"], services["hasher"], services["token"], services["limiter"])
    try:
        result = await uc.execute(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return schemas.TokenResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.post("/auth/refresh", response_model=schemas.TokenResponse)
async def refresh(token: str, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = RefreshToken(services["token"], repos["users"])
    try:
        result = await uc.execute(token)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return schemas.TokenResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


@router.post("/auth/otp")
async def request_otp(phone: str, services=Depends(get_services)):
    uc = RequestOTP(services["otp"], services["limiter"])
    await uc.execute(phone)
    return {"status": "sent"}


@router.post("/auth/otp/verify")
async def verify_otp(user_id: int, phone: str, code: str, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = VerifyOTP(services["otp"], repos["users"])
    ok = await uc.execute(user_id, phone, code)
    if not ok:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"status": "verified"}


@router.post("/auth/reset")
async def reset_password(email: str, new_password: str, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = ResetPassword(repos["users"], services["hasher"])
    ok = await uc.execute(email, new_password)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "reset"}


@router.get("/providers", response_model=list[schemas.ProviderResponse])
async def list_providers(
    category_id: Optional[int] = None,
    city_id: Optional[int] = None,
    area_ids: Optional[str] = None,
    verified: Optional[bool] = None,
    language: Optional[str] = None,
    sort: Optional[str] = None,
    repos=Depends(get_repositories),
    services=Depends(get_services),
):
    area_list = [int(x) for x in area_ids.split(",")] if area_ids else None
    uc = ListProviders(repos["providers"], services["analytics"])
    providers = await uc.execute(
        category_id=category_id,
        city_id=city_id,
        area_ids=area_list,
        verified=verified,
        language=language,
        sort=sort,
    )
    return [schemas.ProviderResponse(**p.__dict__) for p in providers]


@router.get("/providers/{provider_id}", response_model=schemas.ProviderResponse)
async def provider_detail(provider_id: int, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = GetProviderProfile(repos["providers"], services["analytics"])
    provider = await uc.execute(provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Not found")
    return schemas.ProviderResponse(**provider.__dict__)


@router.post("/leads")
async def create_lead(payload: schemas.LeadRequestPayload, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = CreateLeadRequest(repos["leads"], repos["providers"], services["analytics"])
    lead = await uc.execute(
        user_id=0,
        category_id=payload.category_id,
        city_id=payload.city_id,
        area_ids=payload.area_ids,
        description=payload.description,
        preferred_time=payload.preferred_time,
    )
    return {"id": lead.id}


@router.post("/leads/{lead_id}/deliver/{provider_id}")
async def deliver_lead(lead_id: int, provider_id: int, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = DeliverLead(repos["leads"], services["analytics"], repos["subscriptions"])
    delivery = await uc.execute(lead_id=lead_id, provider_id=provider_id)
    return {"delivery_id": delivery.id}


@router.post("/contact-token")
async def contact_token(provider_id: int, user_id: int, lead_id: Optional[int] = None, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = CreateContactToken(repos["contacts"], services["analytics"])
    token = await uc.execute(provider_id, user_id, lead_id)
    return {"contact_token": token}


@router.post("/reviews")
async def create_review(payload: schemas.ReviewPayload, repos=Depends(get_repositories), services=Depends(get_services)):
    uc = CreateReview(repos["leads"], repos["reviews"], repos["providers"], services["analytics"])
    try:
        review = await uc.execute(
            lead_id=payload.lead_id,
            provider_id=payload.provider_id,
            user_id=0,
            rating=payload.rating,
            comment=payload.comment,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"id": review.id}
