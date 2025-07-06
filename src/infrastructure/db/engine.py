from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config

DATABASE_URL = config.db.construct_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=config.db.echo,
    pool_size=config.db.pool_size,
    max_overflow=config.db.max_overflow,
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=config.db.expire_on_commit,
)
