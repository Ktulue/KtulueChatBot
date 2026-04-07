"""Tests for the FastAPI web layer."""
from unittest.mock import patch


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


def test_same_session_id_builds_multi_turn_history(web_client):
    from web.app import sessions

    with patch("web.app.stream_claude_tokens", return_value=iter(["A1"])):
        web_client.post(
            "/api/chat",
            json={"session_id": "multi-1", "message": "first"},
        )
    with patch("web.app.stream_claude_tokens", return_value=iter(["A2"])):
        web_client.post(
            "/api/chat",
            json={"session_id": "multi-1", "message": "second"},
        )

    history = sessions["multi-1"]
    assert len(history) == 4
    assert history[0]["content"] == "first"
    assert history[1]["content"] == "A1"
    assert history[2]["content"] == "second"
    assert history[3]["content"] == "A2"


def test_different_session_ids_have_isolated_histories(web_client):
    from web.app import sessions

    with patch("web.app.stream_claude_tokens", return_value=iter(["X"])):
        web_client.post(
            "/api/chat",
            json={"session_id": "iso-A", "message": "hello A"},
        )
    with patch("web.app.stream_claude_tokens", return_value=iter(["Y"])):
        web_client.post(
            "/api/chat",
            json={"session_id": "iso-B", "message": "hello B"},
        )

    assert len(sessions["iso-A"]) == 2
    assert len(sessions["iso-B"]) == 2
    assert sessions["iso-A"][0]["content"] == "hello A"
    assert sessions["iso-B"][0]["content"] == "hello B"


def test_chat_missing_message_returns_422(web_client):
    response = web_client.post(
        "/api/chat",
        json={"session_id": "v-1"},
    )
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any("message" in str(error["loc"]) for error in body["detail"])


def test_chat_missing_session_id_returns_422(web_client):
    response = web_client.post(
        "/api/chat",
        json={"message": "hi"},
    )
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any("session_id" in str(error["loc"]) for error in body["detail"])


def test_chat_empty_message_returns_422(web_client):
    response = web_client.post(
        "/api/chat",
        json={"session_id": "v-2", "message": ""},
    )
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any("message" in str(error["loc"]) for error in body["detail"])


def test_chat_empty_session_id_returns_422(web_client):
    response = web_client.post(
        "/api/chat",
        json={"session_id": "", "message": "hi"},
    )
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any("session_id" in str(error["loc"]) for error in body["detail"])


def test_chat_error_returns_friendly_message(web_client):
    def raise_error(history):
        # Generators must yield at least once before raising in a way that
        # the StreamingResponse can observe — but raising on first iteration
        # is the realistic Anthropic-error case.
        if False:
            yield ""
        raise RuntimeError("simulated Anthropic API failure")

    with patch("web.app.stream_claude_tokens", side_effect=raise_error):
        response = web_client.post(
            "/api/chat",
            json={"session_id": "err-1", "message": "trigger fail"},
        )

    assert response.status_code == 200
    body = response.text
    # Friendly error must appear in the SSE stream as a data event
    assert '"type": "error"' in body
    # Real exception text must NOT appear
    assert "simulated Anthropic API failure" not in body
    assert "RuntimeError" not in body


def test_chat_error_rolls_back_user_message(web_client):
    from web.app import sessions

    def raise_error(history):
        if False:
            yield ""
        raise RuntimeError("boom")

    with patch("web.app.stream_claude_tokens", side_effect=raise_error):
        web_client.post(
            "/api/chat",
            json={"session_id": "rollback-1", "message": "this should be rolled back"},
        )

    # The user message that triggered the failure must not remain in history
    history = sessions.get("rollback-1", [])
    assert all(
        entry["content"] != "this should be rolled back" for entry in history
    ), f"Expected rollback, but history is {history}"


def test_chat_error_logs_at_error_level(web_client, caplog):
    import logging

    def raise_error(history):
        if False:
            yield ""
        raise RuntimeError("kaboom")

    with caplog.at_level(logging.ERROR, logger="ktulue.web"):
        with patch("web.app.stream_claude_tokens", side_effect=raise_error):
            web_client.post(
                "/api/chat",
                json={"session_id": "log-err-1", "message": "fail me"},
            )

    error_records = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert len(error_records) >= 1
    # Session ID should appear somewhere in the error record for correlation
    assert any("log-err-1" in r.getMessage() for r in error_records)
