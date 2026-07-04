from fastapi import APIRouter, Depends, status

from src.identity.application.dtos.change_password_dto import ChangePasswordInputDto
from src.identity.application.dtos.deactivate_account_dto import DeactivateAccountInputDto
from src.identity.application.use_cases.change_password import ChangePasswordUseCase
from src.identity.application.use_cases.deactivate_account import DeactivateAccountUseCase
from src.identity.presentation.http.api.v1.endpoints.account.models import ChangePasswordRequest
from src.identity.presentation.http.dependencies import (
    get_change_password_use_case,
    get_current_user_id,
    get_deactivate_account_use_case,
)
from src.identity.presentation.http.response import ApiResponse, make_response

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/change-password", response_model=ApiResponse[None])
async def change_password(
    body: ChangePasswordRequest,
    use_case: ChangePasswordUseCase = Depends(get_change_password_use_case),
    user_id=Depends(get_current_user_id),
) -> ApiResponse[None]:
    await use_case.execute(
        ChangePasswordInputDto(
            user_id=user_id,
            current_password=body.current_password,
            new_password=body.new_password,
        )
    )
    return make_response(message="Password changed successfully")


@router.post("/deactivate", status_code=status.HTTP_200_OK, response_model=ApiResponse[None])
async def deactivate_account(
    use_case: DeactivateAccountUseCase = Depends(get_deactivate_account_use_case),
    user_id=Depends(get_current_user_id),
) -> ApiResponse[None]:
    await use_case.execute(DeactivateAccountInputDto(user_id=user_id))
    return make_response(message="Account deactivated")
