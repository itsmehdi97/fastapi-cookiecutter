import pytest
import pytest_asyncio
from unittest import mock

from fastapi.testclient import TestClient

# from core.config import get_settings
from models import mapper_registry
from db.tasks import connect_to_db
from api.server import get_application


# settings = get_settings()


@pytest.fixture
def create_mock_coro(monkeypatch):
    def _create_mock_patch_coro(to_patch=None):
        m = mock.Mock()

        async def _coro(*args, **kwargs):
            return m(*args, **kwargs)

        if to_patch:
            monkeypatch.setattr(to_patch, _coro)
        return m, _coro

    return _create_mock_patch_coro


@pytest_asyncio.fixture
async def memory_session_factory():
    session, engine = await connect_to_db(url="sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield session

    await engine.dispose()


# @pytest_asyncio.fixture
# async def session_factory():
#     session, engine = await connect_to_db(url=settings.DATABASE_URL)
#     async with engine.begin() as conn:
#         await conn.run_sync(mapper_registry.metadata.drop_all)
#         await conn.run_sync(mapper_registry.metadata.create_all)

#     yield session

#     await engine.dispose()


@pytest_asyncio.fixture
async def in_memory_db(memory_session_factory):
    session = memory_session_factory()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def db(session_factory):
    session = session_factory()
    yield session
    await session.close()


@pytest.fixture
def test_client():
    with TestClient(get_application()) as client:
        yield client


# @pytest.fixture
# def uow(memory_session_factory):
#     return SqlAlchemyUnitOfWork(memory_session_factory)
