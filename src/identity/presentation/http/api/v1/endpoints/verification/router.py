from fastapi import APIRouter, Depends

from src.identity.application.dtos.request_password_reset_dto import RequestPasswordResetInputDto
from src.identity.application.dtos.reset_password_dto import ResetPasswordInputDto
from src.identity.application.dtos.verify_email_dto import (
    RequestEmailVerificationInputDto,
    VerifyEmailInputDto,
)
from src.identity.application.use_cases.request_email_verification import RequestEmailVerificationUseCase
from src.identity.application.use_cases.request_password_reset import RequestPasswordResetUseCase
from src.identity.application.use_cases.reset_password import ResetPasswordUseCase
from src.identity.application.use_cases.verify_email import VerifyEmailUseCase
from src.identity.presentation.http.api.v1.endpoints.verification.models import (
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from src.identity.presentation.http.dependencies import (
    get_current_user_id,
    get_request_email_verification_use_case,
    get_request_password_reset_use_case,
    get_reset_password_use_case,
    get_verify_email_use_case,
)
from src.identity.presentation.http.response import ApiResponse, make_response

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/email/request", response_model=ApiResponse[None])
async def request_email_verification(
    use_case: RequestEmailVerificationUseCase = Depends(get_request_email_verification_use_case),
    user_id=Depends(get_current_user_id),
) -> ApiResponse[None]:
    await use_case.execute(RequestEmailVerificationInputDto(user_id=str(user_id)))
    return make_response(message="Verification email sent")


@router.post("/email/verify", response_model=ApiResponse[None])
async def verify_email(
    body: VerifyEmailRequest,
    use_case: VerifyEmailUseCase = Depends(get_verify_email_use_case),
) -> ApiResponse[None]:
    await use_case.execute(VerifyEmailInputDto(verification_token=body.token))
    return make_response(message="Email verified successfully")


@router.post("/password/request-reset", response_model=ApiResponse[None])
async def request_password_reset(
    body: RequestPasswordResetRequest,
    use_case: RequestPasswordResetUseCase = Depends(get_request_password_reset_use_case),
) -> ApiResponse[None]:
    await use_case.execute(RequestPasswordResetInputDto(email=body.email))
    return make_response(message="If that email is registered, a reset link has been sent")


@router.post("/password/reset", response_model=ApiResponse[None])
async def reset_password(
    body: ResetPasswordRequest,
    use_case: ResetPasswordUseCase = Depends(get_reset_password_use_case),
) -> ApiResponse[None]:
    await use_case.execute(ResetPasswordInputDto(reset_token=body.token, new_password=body.new_password))
    return make_response(message="Password reset successfully")
