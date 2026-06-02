"""
Tests for GET /activities endpoint.

Pattern: Arrange-Act-Assert (AAA)
- Arrange: Set up test client via fixture; fixture resets activities state
- Act: Single HTTP request to list activities
- Assert: Validate response structure, status, and content
"""


def test_get_activities_returns_200(client):
    """Test that GET /activities returns status 200."""
    # Arrange: client fixture provides TestClient

    # Act: request the activities endpoint
    response = client.get("/activities")

    # Assert: response is successful
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary of activities."""
    # Arrange: client fixture provides TestClient

    # Act: request the activities endpoint
    response = client.get("/activities")
    data = response.json()

    # Assert: response is a dict (not a list)
    assert isinstance(data, dict)


def test_get_activities_contains_all_nine_activities(client):
    """Test that GET /activities returns all 9 predefined activities."""
    # Arrange: client fixture provides TestClient
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Team",
        "Science Club"
    ]

    # Act: request the activities endpoint
    response = client.get("/activities")
    data = response.json()

    # Assert: all expected activities are present
    assert len(data) == 9
    for activity_name in expected_activities:
        assert activity_name in data


def test_activity_has_required_fields(client):
    """Test that each activity has required fields: description, schedule, max_participants, participants."""
    # Arrange: client fixture provides TestClient
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act: request the activities endpoint
    response = client.get("/activities")
    data = response.json()

    # Assert: each activity has required fields
    for activity_name, activity_data in data.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_participants_field_is_list(client):
    """Test that participants field is a list."""
    # Arrange: client fixture provides TestClient

    # Act: request the activities endpoint
    response = client.get("/activities")
    data = response.json()

    # Assert: participants is a list in each activity
    for activity_name, activity_data in data.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"


def test_chess_club_has_initial_participants(client):
    """Test that Chess Club has expected initial participants."""
    # Arrange: client fixture provides TestClient
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act: request the activities endpoint
    response = client.get("/activities")
    data = response.json()
    chess_participants = data["Chess Club"]["participants"]

    # Assert: Chess Club has expected participants
    assert len(chess_participants) == 2
    assert "michael@mergington.edu" in chess_participants
    assert "daniel@mergington.edu" in chess_participants
