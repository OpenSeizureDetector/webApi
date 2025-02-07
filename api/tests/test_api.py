import pytest


@pytest.mark.anyio
async def test_read_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


@pytest.mark.anyio
async def test_healthcheck(async_client):
    response = await async_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
