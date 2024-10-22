# type: ignore
from typing import Annotated
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Primary Key annotation
pk_int = Annotated[int, mapped_column(primary_key=True)]


# Base class for all models
class ModelBase(AsyncAttrs, DeclarativeBase):
    pass


# Define models
class Course(ModelBase):
    __tablename__ = "courses"

    id: Mapped[pk_int]
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)


# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionFactory = sessionmaker(
    bind=engine,  # Используем bind для привязки движка
    class_=AsyncSession,
    expire_on_commit=False,
)


# Async function to create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
