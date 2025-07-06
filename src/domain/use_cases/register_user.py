from datetime import UTC, datetime

from domain.entities import User
from domain.unit_of_work import UnitOfWork


class RegisterUserUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self,
        social_id: int,
        username: str | None = None,
        name: str | None = None,
        info: str | None = None,
        photo: str | None = None,
    ) -> None:
        async with self.uow:
            existing = await self.uow.user_repo.get_by_social_id(social_id)
            if existing:
                return

            new_user = User(
                id=None,
                social_id=social_id,
                username=username,
                registration_date=datetime.now(UTC),
                taps=0,
                name=name,
                info=info,
                photo=photo,
            )

            await self.uow.user_repo.add(new_user)
