from domain.use_cases import RegisterUserUseCase
from infrastructure.db.engine import session_factory
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


def provide_register_user_use_case() -> RegisterUserUseCase:
    uow = SQLAlchemyUnitOfWork(session_factory)
    return RegisterUserUseCase(uow)
