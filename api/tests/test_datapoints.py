import datetime

import pytest


@pytest.mark.asyncio
async def test_create_datapoint(async_client):
    payload = {
        "dataTime": datetime.datetime.now(datetime.UTC).isoformat(),  # Format ISO 8601
        "statusStr": "Active",  # Obligatoire
        "accMean": 0.95,
        "accSd": 0.02,
        "hr": 72.5,
        "categoryId": 1,
        "eventId": 1,
    }
    response = await async_client.post("/api/datapoints/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["accMean"] == 0.95
    assert data["statusStr"] == "Active"


@pytest.mark.asyncio
async def test_get_datapoints(async_client):
    response = await async_client.get("/api/datapoints/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_datapoint(async_client):
    payload = {
        "dataTime": datetime.datetime.now(datetime.UTC).isoformat(),  # Format ISO 8601
        "statusStr": "Active",
        "accMean": 0.95,
        "accSd": 0.02,
        "hr": 72.5,
        "categoryId": 1,
        "eventId": 1,
    }
    response = await async_client.post("/api/datapoints/", json=payload)
    datapoint_id = response.json()["id"]

    assert response.json()["hr"] == 72.5
    # Mise à jour du datapoint
    update_payload = {"hr": 90}
    response = await async_client.patch(
        f"/api/datapoints/{datapoint_id}", json=update_payload
    )
    assert response.status_code == 200
    assert response.json()["hr"] == 90


@pytest.mark.asyncio
async def test_delete_datapoint(async_client):
    # Création d'un datapoint
    payload = {"name": "To Be Deleted", "value": 99}
    response = await async_client.post("/api/datapoints/", json=payload)
    datapoint_id = response.json()["id"]

    # Suppression du datapoint
    response = await async_client.delete(f"/api/datapoints/{datapoint_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True
