from urllib.parse import quote


def test_signup_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    activity_path = quote(activity_name)

    # Act
    response = client.post(f"/activities/{activity_path}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    activity_path = quote(activity_name)

    # Act
    response = client.delete(f"/activities/{activity_path}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
