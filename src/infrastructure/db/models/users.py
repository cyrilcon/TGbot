from datetime import UTC, datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Text,
)

from infrastructure.db.models.metadata import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("social_id", BigInteger, nullable=False),
    Column("username", String(32)),
    Column("registration_date", DateTime, default=datetime.now(UTC)),
    Column("taps", BigInteger, default=0),
    Column("name", String(64), nullable=True),
    Column("info", Text, nullable=True),
    Column("photo", Text, nullable=True),
)
