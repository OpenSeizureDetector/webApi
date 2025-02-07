import datetime

import pytest


@pytest.mark.asyncio
async def test_create_event(async_client):
    payload = {
        "osdAlarmState": 1,
        "userId": None,
        "dataTime": "2025-02-07T14:30:00Z",
        "type": "Alert",
        "subType": "Critical",
        "desc": "User heart rate anomaly detected.",
    }
    response = await async_client.post("/api/events/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["subType"] == "Critical"


@pytest.mark.asyncio
async def test_get_event(async_client):
    payload = {
        "osdAlarmState": 1,
        "userId": None,
        "dataTime": "2025-02-07T14:30:00Z",
        "type": "Alert",
        "subType": "Critical",
        "desc": "User heart rate anomaly detected.",
    }
    response = await async_client.post("/api/events/", json=payload)
    assert response.status_code == 200
    event_id = response.json()["id"]
    response = await async_client.get(f"/api/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["type"] == "Alert"


@pytest.mark.asyncio
async def test_get_events(async_client):
    response = await async_client.get("/api/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize("update_method_name", ["put", "patch"])
@pytest.mark.asyncio
async def test_update_event(async_client, update_method_name: str):
    payload = {
        "osdAlarmState": 1,
        "userId": None,
        "dataTime": "2025-02-07T14:30:00Z",
        "type": "Alert",
        "subType": "Critical",
        "desc": "User heart rate anomaly detected.",
    }
    response = await async_client.post("/api/events/", json=payload)
    assert response.status_code == 200
    event_id = response.json()["id"]

    assert response.json()["type"] == "Alert"
    update_payload = {"type": "Warning"}

    update_method = getattr(async_client, update_method_name)
    response = await update_method(f"/api/events/{event_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["type"] == "Warning"


@pytest.mark.asyncio
async def test_delete_event(async_client):
    # Création d'un event
    payload = {
        "osdAlarmState": 1,
        "userId": None,
        "dataTime": "2025-02-07T14:30:00Z",
        "type": "Alert",
        "subType": "Critical",
        "desc": "User heart rate anomaly detected.",
    }
    response = await async_client.post("/api/events/", json=payload)
    assert response.status_code == 200
    event_id = response.json()["id"]

    # Suppression du event
    response = await async_client.delete(f"/api/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True
