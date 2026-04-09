from urllib.parse import quote


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activity_path = quote(activity_name)

    # Act
    response = client.delete(f"/activities/{activity_path}/participants?email={email}")
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@mergington.edu"
    activity_path = quote(activity_name)

    # Act
    response = client.delete(f"/activities/{activity_path}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_unregister_signup_cycle(client):
    # Arrange
    activity_name = "Chess Club"
    email = "cycle.student@mergington.edu"
    activity_path = quote(activity_name)

    # Act
    signup_response = client.post(f"/activities/{activity_path}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_path}/participants?email={email}")
    resubscribe_response = client.post(f"/activities/{activity_path}/signup?email={email}")
    activities = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert resubscribe_response.status_code == 200
    assert email in activities[activity_name]["participants"]
