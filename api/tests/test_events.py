import datetime
import pytest_asyncio
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


##### more advanced tests


@pytest_asyncio.fixture(scope="function")
async def insert_events_in_api(async_client):
    """Insert sample events into the API."""
    now = datetime.datetime.now(datetime.UTC)

    payload1 = {
        "dataTime": (now - datetime.timedelta(days=2))
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(),
        "type": "Seizure",
        "subType": "Tonic clonic",
        "desc": "Event 1",
    }
    payload2 = {
        "dataTime": now.replace(tzinfo=datetime.timezone.utc).isoformat(),
        "type": None,
        "subType": None,
        "desc": "Event 2",
    }
    payload3 = {
        "dataTime": (now + datetime.timedelta(days=1))
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(),
        "type": "False Alarm",
        "subType": "Walking",
        "desc": "Event 3",
    }

    response1 = await async_client.post("/api/events/", json=payload1)
    response2 = await async_client.post("/api/events/", json=payload2)
    response3 = await async_client.post("/api/events/", json=payload3)

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200


@pytest.mark.asyncio
async def test_get_all_events(async_client, insert_events_in_api):
    """Test retrieving all events."""
    response = await async_client.get("/api/events/?event_to_categorize=False")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_get_events_order(async_client, insert_events_in_api):
    """Test that events are returned in descending order of dataTime."""
    response = await async_client.get("/api/events/?event_to_categorize=False")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    previous_datetime = None
    for event in data:
        current_datetime = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        if previous_datetime:
            assert current_datetime <= previous_datetime
        previous_datetime = current_datetime


@pytest.mark.asyncio
async def test_get_events_with_start_date(async_client, insert_events_in_api):
    """Test filtering events using start_date."""
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    # Convert start_date to Unix timestamp (in seconds)
    start_timestamp = int(start_date.timestamp())

    response = await async_client.get(
        f"/api/events/?event_to_categorize=False&start_date={start_timestamp}"
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    for event in data:
        event_time = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert event_time >= start_date


@pytest.mark.asyncio
async def test_get_events_with_end_date(async_client, insert_events_in_api):
    """Test filtering events using end_date."""
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    # Convert start_date to Unix timestamp (in seconds)
    end_timestamp = int(end_date.timestamp())

    response = await async_client.get(
        f"/api/events/?event_to_categorize=False&end_date={end_timestamp}"
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    for event in data:
        event_time = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert event_time <= end_date


@pytest.mark.asyncio
async def test_get_events_with_duration(async_client, insert_events_in_api):
    """Test filtering events using duration."""
    duration_minutes = 1440  # 1 jour
    response = await async_client.get(
        f"/api/events/?event_to_categorize=False&duration={duration_minutes}"
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    now = datetime.datetime.now(datetime.UTC)
    min_date = now - datetime.timedelta(minutes=duration_minutes)

    for event in data:
        event_time = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert min_date <= event_time <= now


@pytest.mark.asyncio
async def test_get_events_start_date_duration(async_client, insert_events_in_api):
    """Test filtering events using start_date and duration."""
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    duration_minutes = 120
    start_timestamp = int(start_date.timestamp())

    response = await async_client.get(
        f"/api/events/?event_to_categorize=False&start_date={start_timestamp}&duration={duration_minutes}"
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    min_date = start_date
    max_date = start_date + datetime.timedelta(minutes=duration_minutes)

    for event in data:
        event_time = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert min_date <= event_time <= max_date


@pytest.mark.asyncio
async def test_get_events_end_date_duration(async_client, insert_events_in_api):
    """Test filtering events using end_date and duration."""
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    duration_minutes = 120
    end_timestamp = int(end_date.timestamp())

    response = await async_client.get(
        f"/api/events/?event_to_categorize=False&end_date={end_timestamp}&duration={duration_minutes}"
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    min_date = end_date - datetime.timedelta(minutes=duration_minutes)
    max_date = end_date

    for event in data:
        event_time = datetime.datetime.fromisoformat(event["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert min_date <= event_time <= max_date


@pytest.mark.asyncio
async def test_get_events_to_categorize(async_client, insert_events_in_api):
    """Test filtering events that need to be categorized (type is None)."""
    response = await async_client.get("/api/events/?event_to_categorize=True")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    for event in data:
        assert event["type"] is None


@pytest.mark.asyncio
async def test_get_events_invalid_start_date_future(async_client):
    """Test API error when start_date is in the future."""
    future_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
    future_timestamp = int(future_date.timestamp())

    response = await async_client.get(f"/api/events/?start_date={future_timestamp}")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_events_invalid_duration_negative(async_client):
    """Test API error when duration is negative."""
    response = await async_client.get("/api/events/?duration=-10")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_events_invalid_date_range(async_client):
    """Test API error when end_date is before start_date."""
    start_date = datetime.datetime.now(datetime.UTC)
    end_date = start_date - datetime.timedelta(days=1)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    response = await async_client.get(
        f"/api/events/?start_date={start_timestamp}&end_date={end_timestamp}"
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_events_invalid_event_to_categorize(async_client):
    """Test API error when event_to_categorize has an invalid value."""
    response = await async_client.get("/api/events/?event_to_categorize=invalid_value")
    assert response.status_code == 422
