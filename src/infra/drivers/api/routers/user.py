from fastapi import APIRouter, Depends, status

from core.application.services.user_service import UserService
from core.domain.entities.user import User
from core.domain.exceptions.user_forbidden_error import UserForbiddenError
from infra.drivers.api.dependencies.user import get_authenticated_user, get_user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    user_id: str,
    current_user: User = Depends(get_authenticated_user),
    service: UserService = Depends(get_user_service),
) -> None:
    if user_id != current_user.uid:
        raise UserForbiddenError("Usuário não autorizado a excluir esta conta")
    await service.delete_account(user_id)
