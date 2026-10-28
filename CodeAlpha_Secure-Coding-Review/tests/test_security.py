"""Behavior and security regression tests for the local login application."""
import re
import uuid
from pathlib import Path

import pytest
from werkzeug.security import check_password_hash

from app import create_app
from database import get_user_by_username


@pytest.fixture
def app():
    # Keep test databases outside pytest's --basetemp directory. Pytest clears
    # that directory at startup, which can otherwise race with SQLite setup.
    temp_dir = Path(__file__).resolve().parents[1] / "instance" / "pytest"
    temp_dir.mkdir(parents=True, exist_ok=True)
    database_path = temp_dir / f"test-{uuid.uuid4().hex}.sqlite3"
    test_app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret-key-with-sufficient-length",
        "DATABASE": str(database_path),
        "WTF_CSRF_ENABLED": True,
        "RATELIMIT_STORAGE_URI": "memory://",
    })
    try:
        yield test_app
    finally:
        database_path.unlink(missing_ok=True)


@pytest.fixture
def client(app):
    return app.test_client()


def csrf_token(response):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match, "CSRF token was not rendered in the form"
    return match.group(1).decode()


def post_with_csrf(client, path, data):
    token = csrf_token(client.get(path))
    return client.post(path, data={**data, "csrf_token": token})


def register(client, username="alice", password="correct-horse-battery"):
    return post_with_csrf(client, "/register", {"username": username, "password": password})


def test_registration_stores_password_hash(app, client):
    response = register(client)
    assert response.status_code == 302
    user = get_user_by_username(app.config["DATABASE"], "alice")
    assert user is not None
    assert user["password_hash"] != "correct-horse-battery"
    assert check_password_hash(user["password_hash"], "correct-horse-battery")


def test_valid_login_sets_session_and_allows_dashboard(client):
    register(client)
    response = post_with_csrf(client, "/login", {"username": "alice", "password": "correct-horse-battery"})
    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 200


def test_invalid_login_is_rejected(client):
    register(client)
    response = post_with_csrf(client, "/login", {"username": "alice", "password": "wrong-password"})
    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_login_rate_limit_blocks_excessive_attempts(client):
    token = csrf_token(client.get("/login"))
    form_data = {"username": "alice", "password": "wrong-password", "csrf_token": token}
    for _ in range(5):
        assert client.post("/login", data=form_data).status_code == 401
    assert client.post("/login", data=form_data).status_code == 429


def test_duplicate_username_is_rejected(client):
    assert register(client).status_code == 302
    assert register(client).status_code == 409


@pytest.mark.parametrize("username,password", [
    ("x", "correct-horse-battery"),
    ("bad name", "correct-horse-battery"),
    ("naïve_user", "correct-horse-battery"),
    ("valid_name", "short"),
])
def test_invalid_registration_input_is_rejected(client, username, password):
    assert register(client, username, password).status_code == 400


def test_dashboard_requires_authentication(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.location


def test_logout_clears_session(client):
    register(client)
    post_with_csrf(client, "/login", {"username": "alice", "password": "correct-horse-battery"})
    token = csrf_token(client.get("/dashboard"))
    response = client.post("/logout", data={"csrf_token": token})
    assert response.status_code == 302
    assert client.get("/dashboard").status_code == 302


def test_csrf_blocks_post_without_token(client):
    assert client.post("/register", data={"username": "alice", "password": "correct-horse-battery"}).status_code == 400


def test_template_escapes_username(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "<script>alert(1)</script>"
    page = client.get("/dashboard").data
    assert b"<script>alert(1)</script>" not in page
    assert b"&lt;script&gt;" in page


def test_session_cookie_security_flags(app):
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert app.config["SESSION_COOKIE_SECURE"] is False  # Local HTTP; set COOKIE_SECURE=true for HTTPS.
