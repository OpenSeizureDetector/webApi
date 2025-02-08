import datetime
import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="function")
async def insert_data_in_api(async_client):
    # Create test datapoints with different datetimes
    now = datetime.datetime.now(datetime.UTC)
    payload1 = {
        "dataTime": (now - datetime.timedelta(days=1))
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(),
        "statusStr": "Active",
        "accMean": 0.95,
        "accSd": 0.02,
        "hr": 72.5,
        "categoryId": 1,
    }
    payload2 = {
        "dataTime": now.replace(tzinfo=datetime.timezone.utc).isoformat(),
        "statusStr": "Inactive",
        "accMean": 0.85,
        "accSd": 0.01,
        "hr": 65.0,
        "categoryId": 2,
    }
    payload3 = {
        "dataTime": (now + datetime.timedelta(days=1))
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(),
        "statusStr": "Active",
        "accMean": 0.93,
        "accSd": 0.03,
        "hr": 74.0,
        "categoryId": 3,
    }

    response1 = await async_client.post("/api/datapoints/", json=payload1)
    response2 = await async_client.post("/api/datapoints/", json=payload2)
    response3 = await async_client.post("/api/datapoints/", json=payload3)

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200


@pytest.mark.asyncio
async def test_get_datapoints_summary(async_client, insert_data_in_api):
    # Get datapoints summary
    response = await async_client.get("/api/datapoints/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3  # Ensure at least the two created datapoints are there


@pytest.mark.asyncio
async def test_get_datapoints_summary_order(async_client, insert_data_in_api):
    # Get datapoints summary
    response = await async_client.get("/api/dataSummary/")
    assert response.status_code == 200
    data = response.json()

    # Ensure the data is ordered in descending order of dataTime
    assert isinstance(data, list)
    # Check that the data is sorted by dateTime in descending order
    previous_datetime = None
    for datapoint in data:
        current_datetime = datetime.datetime.fromisoformat(
            datapoint["dataTime"]
        ).replace(tzinfo=datetime.timezone.utc)
        if previous_datetime:
            assert current_datetime <= previous_datetime
        previous_datetime = current_datetime


@pytest.mark.asyncio
async def test_get_datapoints_with_start_date(async_client, insert_data_in_api):
    # Set start date (e.g., one day ago)
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)

    # Convert start_date to Unix timestamp (in seconds)
    start_timestamp = int(start_date.timestamp())

    # Get datapoints with start_date filter
    response = await async_client.get(f"/api/dataSummary/?start_date={start_timestamp}")
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints after the start_date
    assert isinstance(data, list)
    assert len(data) == 2  # There should be datapoints after start_date
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert datapoint_time.timestamp() >= start_timestamp


@pytest.mark.asyncio
async def test_get_datapoints_with_end_date(async_client, insert_data_in_api):
    # Set end date (e.g., one day from now)
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)

    # Convert end_date to Unix timestamp (in seconds)
    end_timestamp = int(end_date.timestamp())

    # Get datapoints with end_date filter
    response = await async_client.get(f"/api/dataSummary/?end_date={end_timestamp}")
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints before the end_date
    assert isinstance(data, list)
    assert len(data) == 2  # There should be datapoints before end_date
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert datapoint_time.timestamp() <= end_timestamp


@pytest.mark.asyncio
async def test_get_datapoints_with_start_and_end_date(async_client, insert_data_in_api):
    # Set start and end date (e.g., from one day ago to one day from now)
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)

    # Convert both start_date and end_date to Unix timestamps (in seconds)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    # Get datapoints within the date range
    response = await async_client.get(
        f"/api/dataSummary/?start_date={start_timestamp}&end_date={end_timestamp}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints between start_date and end_date
    assert isinstance(data, list)
    assert len(data) == 1  # There should be datapoints within the date range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = int(datapoint_time.timestamp())
        assert start_timestamp <= datapoint_timestamp <= end_timestamp


@pytest.mark.asyncio
async def test_get_datapoints_with_start_date_and_duration(
    async_client, insert_data_in_api
):
    # Set start date (e.g., one day ago) and duration (e.g., 2 days)
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    duration_seconds = 2 * 24 * 60 * 60  # 2 days in seconds

    # Convert start_date to Unix timestamp (in seconds)
    start_timestamp = int(start_date.timestamp())

    # Get datapoints from start_date with duration filter
    response = await async_client.get(
        f"/api/dataSummary/?start_date={start_timestamp}&duration_min={duration_seconds}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints that meet the duration requirement
    assert isinstance(data, list)
    assert len(data) > 0  # There should be datapoints within the duration range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = int(datapoint_time.timestamp())
        assert datapoint_timestamp >= start_timestamp
        # Check that the duration between start_date and datapoint is less than duration_min
        assert (datapoint_timestamp - start_timestamp) <= duration_seconds


@pytest.mark.asyncio
async def test_get_datapoints_with_end_date_and_duration(
    async_client, insert_data_in_api
):
    # Set end date (e.g., one day from now) and duration (e.g., 2 days)
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    duration_seconds = 2 * 24 * 60 * 60  # 2 days in seconds

    # Convert end_date to Unix timestamp (in seconds)
    end_timestamp = int(end_date.timestamp())

    # Get datapoints before end_date with duration filter
    response = await async_client.get(
        f"/api/dataSummary/?end_date={end_timestamp}&duration_min={duration_seconds}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints before the end_date and that meet the duration requirement
    assert isinstance(data, list)
    assert (
        len(data) > 0
    )  # There should be datapoints before the end_date and within the duration range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = int(datapoint_time.timestamp())
        assert datapoint_timestamp <= end_timestamp
        # Check that the duration between end_date and datapoint is greater than duration_min
        assert (end_timestamp - datapoint_timestamp) <= duration_seconds


@pytest.mark.asyncio
async def test_get_datapoints_with_start_date_str(async_client, insert_data_in_api):
    # Set start date (e.g., 1 hour ago) as string
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string

    # Get datapoints with startDateStr filter
    response = await async_client.get(
        f"/api/dataSummary/?startDateStr={start_date_str}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints after the start_date
    assert isinstance(data, list)
    assert len(data) == 2  # There should be datapoints after start_date
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert datapoint_time.timestamp() >= start_date.timestamp()


@pytest.mark.asyncio
async def test_get_datapoints_with_end_date_str(async_client, insert_data_in_api):
    # Set end date (e.g., 1 hour from now) as string
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string

    # Get datapoints with endDateStr filter
    response = await async_client.get(f"/api/dataSummary/?endDateStr={end_date_str}")
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints before the end_date
    assert isinstance(data, list)
    assert len(data) > 0  # There should be datapoints before end_date
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        assert datapoint_time.timestamp() <= end_date.timestamp()


@pytest.mark.asyncio
async def test_get_datapoints_with_start_and_end_date_str(
    async_client, insert_data_in_api
):
    # Set start and end date (e.g., from 1 hour ago to 1 hour from now) as strings
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string

    # Get datapoints within the date range
    response = await async_client.get(
        f"/api/dataSummary/?startDateStr={start_date_str}&endDateStr={end_date_str}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints between start_date and end_date
    assert isinstance(data, list)
    assert len(data) > 0  # There should be datapoints within the date range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = int(datapoint_time.timestamp())
        assert start_date.timestamp() <= datapoint_timestamp <= end_date.timestamp()


@pytest.mark.asyncio
async def test_get_datapoints_with_start_date_str_and_duration(
    async_client, insert_data_in_api
):
    # Set start date (e.g., 1 hour ago) as string and duration (e.g., 2 hours in minutes)
    start_date = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
    duration_minutes = 120  # 2 hours in minutes
    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string

    # Get datapoints from start_date with durationMinStr filter
    response = await async_client.get(
        f"/api/dataSummary/?startDateStr={start_date_str}&durationMinStr={duration_minutes}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints that meet the duration requirement
    assert isinstance(data, list)
    assert len(data) > 0  # There should be datapoints within the duration range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = datapoint_time.timestamp()
        start_date_timestamp = start_date.timestamp()
        assert datapoint_timestamp >= start_date_timestamp
        # Check that the duration between start_date and datapoint is less than duration_min
        assert (datapoint_timestamp - start_date_timestamp) <= duration_minutes * 60


@pytest.mark.asyncio
async def test_get_datapoints_with_end_date_str_and_duration(
    async_client, insert_data_in_api
):
    # Set end date (e.g., 1 hour from now) as string and duration (e.g., 2 hours in minutes)
    end_date = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    duration_minutes = 120  # 2 hours in minutes
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")  # Format as string

    # Get datapoints before end_date with durationMinStr filter
    response = await async_client.get(
        f"/api/dataSummary/?endDateStr={end_date_str}&durationMinStr={duration_minutes}"
    )
    assert response.status_code == 200
    data = response.json()

    # Ensure the data contains only datapoints before the end_date and that meet the duration requirement
    assert isinstance(data, list)
    assert (
        len(data) > 0
    )  # There should be datapoints before the end_date and within the duration range
    for datapoint in data:
        datapoint_time = datetime.datetime.fromisoformat(datapoint["dataTime"]).replace(
            tzinfo=datetime.timezone.utc
        )
        datapoint_timestamp = int(datapoint_time.timestamp())
        assert datapoint_timestamp <= end_date.timestamp()
        # Check that the duration between end_date and datapoint is greater than duration_min
        assert (end_date.timestamp() - datapoint_timestamp) <= duration_minutes * 60
