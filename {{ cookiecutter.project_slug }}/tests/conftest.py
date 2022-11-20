import pytest
import pytest_asyncio
from unittest import mock

from models import mapper_registry
from db.tasks import connect_to_db


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
