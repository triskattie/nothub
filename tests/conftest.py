import asyncio
import os
from collections.abc import AsyncIterator, Iterator
import pytest
from alembic import command
from alembic.config import Config
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool
from api.db.session import get_db
from api.main import app


TEST_DATABASE_URL = os.environ["DATABASE_URL"]

database_url = make_url(TEST_DATABASE_URL)
database_name = database_url.database

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)


async def create_test_database() -> None:
    admin_engine = create_async_engine(
        database_url.set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )

    async with admin_engine.connect() as connection:
        result = await connection.execute(
            text(
                """
                SELECT 1
                FROM pg_database
                WHERE datname = :name
                """
            ),
            {"name": database_name},
        )

        if result.scalar_one_or_none() is None:
            await connection.exec_driver_sql(
                f'CREATE DATABASE "{database_name}"'
            )

    await admin_engine.dispose()


def run_migrations() -> None:
    command.upgrade(Config("alembic.ini"), "head")


@pytest.fixture(scope="session", autouse=True)
def prepare_database() -> Iterator[None]:
    asyncio.run(create_test_database())
    run_migrations()

    yield

    asyncio.run(test_engine.dispose())


@pytest.fixture
async def db_session(
    prepare_database: None,
) -> AsyncIterator[AsyncSession]:
    async with test_engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncIterator[AsyncClient]:
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"