from core.domain.entities.user import User
from core.domain.exceptions.user_not_found_error import UserNotFoundError
from core.ports.auth.auth_service import IAuthService
from core.ports.repositories.user_repository import IUserRepository


class UserService:
    def __init__(
        self, user_repository: IUserRepository, auth_service: IAuthService
    ) -> None:
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def get_or_create_user(self, user: User) -> User:
        existing_user = await self.user_repository.find_by_id(user.uid)
        if existing_user:
            return existing_user
        return await self.user_repository.save(user)

    async def delete_account(self, uid: str) -> None:
        existing_user = await self.user_repository.find_by_id(uid)
        if not existing_user:
            raise UserNotFoundError(f"Usuário não encontrado: {uid}")
        await self.auth_service.delete_user(uid)
        await self.user_repository.delete(uid)
