import pytest


@pytest.mark.asyncio
async def test_get(test_client):
    result = test_client.post(
        '/api/tasks/',
        json={"title": "some title", "desc": "some desc"})
    assert result.status_code == 200
