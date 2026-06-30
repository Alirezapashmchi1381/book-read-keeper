from fastapi import APIRouter, HTTPException, status

from src.api.dependencies.identity import (
    ChangePasswordUseCaseDep,
    CurrentUserDep,
    DeactivateAccountUseCaseDep,
    LoginUseCaseDep,
    LogoutAllDevicesUseCaseDep,
    LogoutUseCaseDep,
    RefreshTokenUseCaseDep,
    RequestEmailVerificationUseCaseDep,
    RequestPasswordResetUseCaseDep,
    ResetPasswordUseCaseDep,
    SignupUseCaseDep,
    VerifyEmailUseCaseDep,
)
from src.identity.application.dtos.change_password_dto import ChangePasswordInputDto
from src.identity.application.dtos.deactivate_account_dto import DeactivateAccountInputDto
from src.identity.application.dtos.login_dto import LoginInputDto
from src.identity.application.dtos.logout_dto import LogoutAllDevicesInputDto, LogoutInputDto
from src.identity.application.dtos.refresh_token_dto import RefreshTokenInputDto
from src.identity.application.dtos.request_password_reset_dto import RequestPasswordResetInputDto
from src.identity.application.dtos.reset_password_dto import ResetPasswordInputDto
from src.identity.application.dtos.signup_dto import SignupInputDto
from src.identity.application.dtos.verify_email_dto import RequestEmailVerificationInputDto, VerifyEmailInputDto
from src.identity.presentation.models import (
    AuthResponse,
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    SignupRequest,
    TokenResponse,
    VerifyEmailRequest,
)

router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: SignupRequest, use_case: SignupUseCaseDep) -> AuthResponse:
    try:
        result = await use_case.execute(SignupInputDto(
            email=body.email,
            username=body.username,
            password=body.password,
        ))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return AuthResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        user_id=result.user_id,
        username=result.username,
        email=result.email,
    )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, use_case: LoginUseCaseDep) -> AuthResponse:
    try:
        result = await use_case.execute(LoginInputDto(
            email=body.email,
            password=body.password,
        ))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return AuthResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        user_id=result.user_id,
        username=result.username,
        email=result.email,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: LogoutRequest, use_case: LogoutUseCaseDep) -> None:
    await use_case.execute(LogoutInputDto(refresh_token=body.refresh_token))


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all_devices(
    use_case: LogoutAllDevicesUseCaseDep,
    current_user: CurrentUserDep,
) -> None:
    await use_case.execute(LogoutAllDevicesInputDto(user_id=current_user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshTokenRequest, use_case: RefreshTokenUseCaseDep) -> TokenResponse:
    try:
        result = await use_case.execute(RefreshTokenInputDto(refresh_token=body.refresh_token))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return TokenResponse(access_token=result.access_token, refresh_token=result.refresh_token)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    body: ChangePasswordRequest,
    use_case: ChangePasswordUseCaseDep,
    current_user: CurrentUserDep,
) -> None:
    try:
        await use_case.execute(ChangePasswordInputDto(
            user_id=current_user,
            current_password=body.current_password,
            new_password=body.new_password,
        ))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/account", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_account(
    use_case: DeactivateAccountUseCaseDep,
    current_user: CurrentUserDep,
) -> None:
    try:
        await use_case.execute(DeactivateAccountInputDto(user_id=current_user))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/password-reset/request", status_code=status.HTTP_204_NO_CONTENT)
async def request_password_reset(
    body: RequestPasswordResetRequest,
    use_case: RequestPasswordResetUseCaseDep,
) -> None:
    await use_case.execute(RequestPasswordResetInputDto(email=body.email))


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(body: ResetPasswordRequest, use_case: ResetPasswordUseCaseDep) -> None:
    try:
        await use_case.execute(ResetPasswordInputDto(
            reset_token=body.reset_token,
            new_password=body.new_password,
        ))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/email-verification/request", status_code=status.HTTP_204_NO_CONTENT)
async def request_email_verification(
    use_case: RequestEmailVerificationUseCaseDep,
    current_user: CurrentUserDep,
) -> None:
    try:
        await use_case.execute(RequestEmailVerificationInputDto(user_id=str(current_user)))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/email-verification/confirm", status_code=status.HTTP_204_NO_CONTENT)
async def verify_email(body: VerifyEmailRequest, use_case: VerifyEmailUseCaseDep) -> None:
    try:
        await use_case.execute(VerifyEmailInputDto(verification_token=body.verification_token))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
