"""Tests for the FastAPI web layer."""


def test_root_returns_html(web_client):
    response = web_client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<html" in response.text.lower()


def test_root_contains_chat_container(web_client):
    response = web_client.get("/")
    assert "chat" in response.text.lower()


def test_static_styles_served(web_client):
    response = web_client.get("/static/styles.css")
    assert response.status_code == 200
    assert "css" in response.headers["content-type"].lower()


def test_static_chat_js_served(web_client):
    response = web_client.get("/static/chat.js")
    assert response.status_code == 200
    # Browsers accept several MIME types for JS; just verify it loads.
