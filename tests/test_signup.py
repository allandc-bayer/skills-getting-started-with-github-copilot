"""
Tests for POST /activities/{activity_name}/signup endpoint.

Pattern: Arrange-Act-Assert (AAA)
- Arrange: Set up test client and initial state (via fixtures)
- Act: Single POST request to signup endpoint
- Assert: Validate response status and participant list mutation
"""


def test_signup_success_adds_participant(client):
    """Test that signing up a new student adds them to participants."""
    # Arrange: client fixture provides TestClient with reset activities
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act: sign up new student
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: response is successful and participant count increased
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_returns_success_message(client):
    """Test that successful signup returns appropriate message."""
    # Arrange: client fixture provides TestClient
    activity_name = "Programming Class"
    email = "alice@mergington.edu"

    # Act: sign up student
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: response contains success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for non-existent activity returns 404."""
    # Arrange: client fixture provides TestClient
    nonexistent_activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act: attempt to sign up for non-existent activity
    response = client.post(f"/activities/{nonexistent_activity}/signup", params={"email": email})

    # Assert: response is 404 not found
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_returns_400(client):
    """Test that duplicate signup returns 400 bad request."""
    # Arrange: client fixture provides TestClient
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up for Chess Club

    # Act: attempt to sign up already-registered student
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: response is 400 bad request
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_duplicate_does_not_add_duplicate(client):
    """Test that duplicate signup does not add student twice."""
    # Arrange: client fixture provides TestClient
    activity_name = "Tennis Club"
    email = "jessica@mergington.edu"  # Already signed up
    initial_participants = client.get("/activities").json()[activity_name]["participants"].copy()

    # Act: attempt duplicate signup
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: participant list is unchanged
    updated_participants = client.get("/activities").json()[activity_name]["participants"]
    assert len(updated_participants) == len(initial_participants)
    assert updated_participants.count(email) == 1


def test_multiple_different_students_can_signup(client):
    """Test that multiple different students can sign up for same activity."""
    # Arrange: client fixture provides TestClient
    activity_name = "Gym Class"
    new_emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act: sign up multiple different students
    for email in new_emails:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
        assert response.status_code == 200

    # Assert: all students were added
    updated_activities = client.get("/activities").json()
    final_count = len(updated_activities[activity_name]["participants"])
    assert final_count == initial_count + len(new_emails)
    for email in new_emails:
        assert email in updated_activities[activity_name]["participants"]


def test_signup_preserves_other_activities(client):
    """Test that signing up for one activity doesn't affect other activities."""
    # Arrange: client fixture provides TestClient
    target_activity = "Drama Club"
    other_activity = "Art Studio"
    email = "newstudent@mergington.edu"
    
    other_activity_before = client.get("/activities").json()[other_activity]["participants"].copy()

    # Act: sign up for one activity
    client.post(f"/activities/{target_activity}/signup", params={"email": email})

    # Assert: other activities unchanged
    other_activity_after = client.get("/activities").json()[other_activity]["participants"]
    assert other_activity_before == other_activity_after
    assert email not in other_activity_after
