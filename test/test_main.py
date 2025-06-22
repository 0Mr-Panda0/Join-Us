import pytest
from unittest.mock import patch
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("main.users_table_creation")
@patch("main.count_users")
@patch("main.insert_fake_email")
@patch("main.render_template")
def test_index_inserts_fake_email_when_no_users(
    mock_render_template,
    mock_insert_fake_email,
    mock_count_users,
    mock_users_table_creation,
    client,
):
    mock_count_users.return_value = 0
    mock_render_template.return_value = "rendered"
    response = client.get("/")
    mock_users_table_creation.assert_called_once()
    mock_count_users.assert_called_once()
    mock_insert_fake_email.assert_called_once()
    mock_render_template.assert_called_with("hello.html", count=0)
    assert response.data == b"rendered"


@patch("main.users_table_creation")
@patch("main.count_users")
@patch("main.insert_fake_email")
@patch("main.render_template")
def test_index_does_not_insert_fake_email_when_users_exist(
    mock_render_template,
    mock_insert_fake_email,
    mock_count_users,
    mock_users_table_creation,
    client,
):
    mock_count_users.return_value = 5
    mock_render_template.return_value = "rendered"
    response = client.get("/")
    mock_users_table_creation.assert_called_once()
    mock_count_users.assert_called_once()
    mock_insert_fake_email.assert_not_called()
    mock_render_template.assert_called_with("hello.html", count=5)
    assert response.data == b"rendered"


@patch("main.insert_email")
def test_join_post_inserts_email_and_redirects(mock_insert_email, client):
    response = client.post("/join", data={"email": "test@example.com"})
    mock_insert_email.assert_called_once_with("test@example.com")
    # Should redirect (302) to "/"
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_index_route_method_allowed(client):
    response = client.get("/")
    assert response.status_code == 200


def test_join_route_method_not_allowed(client):
    response = client.get("/join")
    assert response.status_code == 405
