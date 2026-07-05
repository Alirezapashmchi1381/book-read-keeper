from fastapi import APIRouter, Depends, status

from src.identity.application.dtos.login_dto import LoginInputDto
from src.identity.application.dtos.logout_dto import LogoutAllDevicesInputDto, LogoutInputDto
from src.identity.application.dtos.refresh_token_dto import RefreshTokenInputDto
from src.identity.application.dtos.signup_dto import SignupInputDto
from src.identity.application.use_cases.login import LoginUseCase
from src.identity.application.use_cases.logout import LogoutUseCase
from src.identity.application.use_cases.logout_all_devices import LogoutAllDevicesUseCase
from src.identity.application.use_cases.refresh_token import RefreshTokenUseCase
from src.identity.application.use_cases.signup import SignupUseCase
from src.identity.presentation.http.api.v1.endpoints.auth.models import (
    AuthResponse,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
    SignupRequest,
)
from src.identity.core.dependencies import (
    get_login_use_case,
    get_logout_all_devices_use_case,
    get_logout_use_case,
    get_refresh_token_use_case,
    get_signup_use_case,
    get_current_user_id
)
from src.identity.presentation.http.response import ApiResponse, make_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[AuthResponse],
)
async def signup(
    body: SignupRequest,
    use_case: SignupUseCase = Depends(get_signup_use_case),
) -> ApiResponse[AuthResponse]:
    result = await use_case.execute(
        SignupInputDto(email=body.email, username=body.username, password=body.password)
    )
    return make_response(
        data=AuthResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            user_id=str(result.user_id),
            username=result.username,
            email=result.email,
        ),
        message="Account created successfully",
        code=status.HTTP_201_CREATED,
    )


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(
    body: LoginRequest,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> ApiResponse[AuthResponse]:
    result = await use_case.execute(LoginInputDto(email=body.email, password=body.password))
    return make_response(
        data=AuthResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            user_id=str(result.user_id),
            username=result.username,
            email=result.email,
        ),
        message="Login successful",
    )


@router.post("/logout", response_model=ApiResponse[None])
async def logout(
    body: LogoutRequest,
    use_case: LogoutUseCase = Depends(get_logout_use_case),
) -> ApiResponse[None]:
    await use_case.execute(LogoutInputDto(refresh_token=body.refresh_token))
    return make_response(message="Logged out successfully")


@router.post("/logout-all", response_model=ApiResponse[None])
async def logout_all_devices(
    use_case: LogoutAllDevicesUseCase = Depends(get_logout_all_devices_use_case),
    user_id=Depends(get_current_user_id),
) -> ApiResponse[None]:
    await use_case.execute(LogoutAllDevicesInputDto(user_id=user_id))
    return make_response(message="Logged out from all devices")


@router.post("/refresh", response_model=ApiResponse[RefreshTokenResponse])
async def refresh_token(
    body: RefreshTokenRequest,
    use_case: RefreshTokenUseCase = Depends(get_refresh_token_use_case),
) -> ApiResponse[RefreshTokenResponse]:
    result = await use_case.execute(RefreshTokenInputDto(refresh_token=body.refresh_token))
    return make_response(
        data=RefreshTokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
        ),
        message="Token refreshed",
    )
