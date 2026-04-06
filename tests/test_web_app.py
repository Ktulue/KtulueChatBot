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


from unittest.mock import patch


def test_chat_endpoint_streams_tokens(web_client):
    fake_tokens = ["Hello", " ", "Josh!"]

    with patch("web.app.stream_claude_tokens", return_value=iter(fake_tokens)):
        response = web_client.post(
            "/api/chat",
            json={"session_id": "session-A", "message": "hi"},
        )

    assert response.status_code == 200
    body = response.text
    assert "Hello" in body
    assert "Josh!" in body
    # SSE events look like: data: {"type": "token", "text": "Hello"}\n\n
    assert body.count("data:") >= len(fake_tokens)


def test_chat_endpoint_records_user_and_assistant_history(web_client):
    from web.app import sessions

    fake_tokens = ["Hi", " there"]

    with patch("web.app.stream_claude_tokens", return_value=iter(fake_tokens)):
        web_client.post(
            "/api/chat",
            json={"session_id": "session-B", "message": "hello"},
        )

    history = sessions["session-B"]
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "hello"}
    assert history[1] == {"role": "assistant", "content": "Hi there"}
