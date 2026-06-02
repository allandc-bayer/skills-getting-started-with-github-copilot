"""
Shared test fixtures for FastAPI backend tests.

Uses Arrange-Act-Assert pattern:
- Fixtures prepare the test environment (Arrange)
- Test functions perform a single action (Act)
- Test functions validate outcomes (Assert)
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI app.
    
    Arrange: Returns a TestClient instance ready for testing.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets activities to a known state before and after each test.
    
    Arrange: Establishes deterministic initial state (deep copy of original data).
    Ensures test isolation and prevents state leakage across test functions.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for varsity and JV levels",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn and practice tennis skills on the school courts",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["jessica@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in school plays and theatrical productions",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["rachel@mergington.edu", "james@mergington.edu"]
        },
        "Art Studio": {
            "description": "Create paintings, drawings, and sculptures in a studio setting",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["sarah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in formal debates and develop public speaking skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["thomas@mergington.edu", "lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore STEM concepts through hands-on projects",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["kevin@mergington.edu"]
        }
    }
    
    # Reset activities before test runs
    activities.clear()
    activities.update(original_activities)
    
    # Yield control to the test function
    yield
    
    # Reset activities after test completes
    activities.clear()
    activities.update(original_activities)
