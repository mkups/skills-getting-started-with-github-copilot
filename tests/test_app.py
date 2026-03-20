from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    """Test that root endpoint redirects to static index.html"""
    # Arrange: No special setup needed

    # Act: Make GET request to root without following redirect
    response = client.get("/", follow_redirects=False)

    # Assert: Should redirect to /static/index.html
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """Test retrieving all activities"""
    # Arrange: No special setup needed

    # Act: Make GET request to activities endpoint
    response = client.get("/activities")

    # Assert: Should return 200 and a dictionary of activities
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Should have activities

    # Check structure of first activity
    first_activity = next(iter(data.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)


def test_signup_successful():
    """Test successful signup for an activity"""
    # Arrange: Choose an activity and email not already signed up
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_already_signed_up():
    """Test signup when student is already signed up"""
    # Arrange: Use an activity and email that's already in the data
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # From initial data

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_invalid_activity():
    """Test signup for non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_unregister_successful():
    """Test successful unregister from an activity"""
    # Arrange: Use an activity and email that's signed up
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # From initial data

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Should return 200 and success message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_not_signed_up():
    """Test unregister when student is not signed up"""
    # Arrange: Use an activity and email that's not signed up
    activity_name = "Programming Class"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_invalid_activity():
    """Test unregister from non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]