import pytest
import pytest_asyncio

from fastapi.testclient import TestClient

from models import mapper_registry
from db.tasks import connect_to_db
from core.config import get_settings
from api.server import get_application


settings = get_settings()


@pytest.fixture
def test_client():
    with TestClient(get_application()) as client:
        yield client


@pytest_asyncio.fixture(autouse=True, scope="function")
async def fresh_db():
    _, engine = await connect_to_db(url=settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield

    await engine.dispose()
