from core.domain.entities.user import User
from core.ports.repositories.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    async def get_or_create_user(self, user: User) -> User:
        existing_user = await self.user_repository.find_by_id(user.uid)
        if existing_user:
            return existing_user
        return await self.user_repository.save(user)
