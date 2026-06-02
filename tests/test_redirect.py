"""
Tests for GET / endpoint (root redirect).

Pattern: Arrange-Act-Assert (AAA)
- Arrange: Set up test client via fixture
- Act: Single HTTP request to the endpoint
- Assert: Validate response status and headers
"""


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html."""
    # Arrange: client fixture provides TestClient
    
    # Act: request the root endpoint
    response = client.get("/", follow_redirects=False)
    
    # Assert: response is a redirect (307 or 308)
    assert response.status_code in [307, 308]
    assert response.headers.get("location") == "/static/index.html"


def test_root_redirect_location_header_exists(client):
    """Test that redirect includes location header."""
    # Arrange: client fixture provides TestClient
    
    # Act: request the root endpoint without following redirects
    response = client.get("/", follow_redirects=False)
    
    # Assert: response includes location header pointing to static files
    assert "location" in response.headers
    assert response.is_redirect
