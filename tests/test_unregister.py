"""
Tests for DELETE /activities/{activity_name}/participants endpoint.

Pattern: Arrange-Act-Assert (AAA)
- Arrange: Set up test client and initial state (via fixtures)
- Act: Single DELETE request to unregister endpoint
- Assert: Validate response status and participant list mutation
"""


def test_unregister_success_removes_participant(client):
    """Test that unregistering a student removes them from participants."""
    # Arrange: client fixture provides TestClient with reset activities
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Known participant in Chess Club
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act: unregister student
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: response is successful and participant count decreased
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_returns_success_message(client):
    """Test that successful unregister returns appropriate message."""
    # Arrange: client fixture provides TestClient
    activity_name = "Tennis Club"
    email = "jessica@mergington.edu"  # Known participant

    # Act: unregister student
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: response contains success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from non-existent activity returns 404."""
    # Arrange: client fixture provides TestClient
    nonexistent_activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act: attempt to unregister from non-existent activity
    response = client.delete(f"/activities/{nonexistent_activity}/participants", params={"email": email})

    # Assert: response is 404 not found
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant_returns_404(client):
    """Test that unregistering non-existent participant returns 404."""
    # Arrange: client fixture provides TestClient
    activity_name = "Basketball Team"
    email = "notamember@mergington.edu"  # Not signed up

    # Act: attempt to unregister non-existent participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: response is 404 not found
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_nonexistent_participant_preserves_activity(client):
    """Test that failed unregister doesn't affect activity participants."""
    # Arrange: client fixture provides TestClient
    activity_name = "Debate Team"
    email = "notamember@mergington.edu"
    
    activity_before = client.get("/activities").json()[activity_name]["participants"].copy()

    # Act: attempt to unregister non-existent participant
    client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: activity participants unchanged
    activity_after = client.get("/activities").json()[activity_name]["participants"]
    assert activity_before == activity_after


def test_unregister_one_participant_keeps_others(client):
    """Test that unregistering one participant keeps others."""
    # Arrange: client fixture provides TestClient
    activity_name = "Drama Club"
    email_to_remove = "rachel@mergington.edu"
    email_to_keep = "james@mergington.edu"
    
    initial_participants = client.get("/activities").json()[activity_name]["participants"].copy()
    assert email_to_remove in initial_participants
    assert email_to_keep in initial_participants

    # Act: unregister one participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email_to_remove})

    # Assert: removed participant is gone, but other remains
    assert response.status_code == 200
    updated_participants = client.get("/activities").json()[activity_name]["participants"]
    assert email_to_remove not in updated_participants
    assert email_to_keep in updated_participants
    assert len(updated_participants) == len(initial_participants) - 1


def test_unregister_preserves_other_activities(client):
    """Test that unregistering from one activity doesn't affect other activities."""
    # Arrange: client fixture provides TestClient
    target_activity = "Science Club"
    other_activity = "Programming Class"
    email = "kevin@mergington.edu"  # Signed up for Science Club
    
    other_activity_before = client.get("/activities").json()[other_activity]["participants"].copy()

    # Act: unregister from one activity
    client.delete(f"/activities/{target_activity}/participants", params={"email": email})

    # Assert: other activities unchanged
    other_activity_after = client.get("/activities").json()[other_activity]["participants"]
    assert other_activity_before == other_activity_after


def test_multiple_unregisters_from_same_activity(client):
    """Test that multiple students can be unregistered from the same activity."""
    # Arrange: client fixture provides TestClient
    activity_name = "Gym Class"
    email1 = "john@mergington.edu"
    email2 = "olivia@mergington.edu"
    
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act: unregister multiple students
    response1 = client.delete(f"/activities/{activity_name}/participants", params={"email": email1})
    response2 = client.delete(f"/activities/{activity_name}/participants", params={"email": email2})

    # Assert: both were successfully removed
    assert response1.status_code == 200
    assert response2.status_code == 200
    updated_activities = client.get("/activities").json()
    final_count = len(updated_activities[activity_name]["participants"])
    assert final_count == initial_count - 2
    assert email1 not in updated_activities[activity_name]["participants"]
    assert email2 not in updated_activities[activity_name]["participants"]
