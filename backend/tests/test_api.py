def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_register(client):
    resp = client.post(
        "/api/v1/users/register",
        json={"email": "test@example.com", "full_name": "Test User", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "full_name": "Dup User", "password": "pass"}
    client.post("/api/v1/users/register", json=payload)
    resp = client.post("/api/v1/users/register", json=payload)
    assert resp.status_code == 400


def test_login_and_me(client):
    client.post(
        "/api/v1/users/register",
        json={"email": "user@example.com", "full_name": "User", "password": "pass123"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "user@example.com", "password": "pass123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    me_resp = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "user@example.com"


def test_login_wrong_password(client):
    client.post(
        "/api/v1/users/register",
        json={"email": "a@example.com", "full_name": "A", "password": "correct"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": "a@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def _register_and_login(client, email="e@example.com", password="pw"):
    client.post(
        "/api/v1/users/register",
        json={"email": email, "full_name": "Name", "password": password},
    )
    resp = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


def test_create_and_list_events(client):
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(
        "/api/v1/events/",
        json={"title": "Meeting", "start_time": "2024-06-01T10:00:00"},
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["title"] == "Meeting"

    list_resp = client.get("/api/v1/events/", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_update_event(client):
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/api/v1/events/",
        json={"title": "Old Title", "start_time": "2024-06-01T10:00:00"},
        headers=headers,
    )
    event_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/api/v1/events/{event_id}",
        json={"title": "New Title"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New Title"


def test_delete_event(client):
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/api/v1/events/",
        json={"title": "To Delete", "start_time": "2024-06-01T10:00:00"},
        headers=headers,
    )
    event_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/v1/events/{event_id}", headers=headers)
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/v1/events/{event_id}", headers=headers)
    assert get_resp.status_code == 404
