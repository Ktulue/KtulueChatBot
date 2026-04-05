from unittest.mock import patch, MagicMock

from main import send_message, create_client


def test_create_client_returns_anthropic_client():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
        client = create_client()
    assert client is not None


def test_send_message_returns_response_text():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="Hey there! Welcome to the stream.")
    ]

    history = []
    result = send_message(mock_client, "system prompt", history, "Hello!", stream=False)

    assert result == "Hey there! Welcome to the stream."
    assert len(history) == 2  # user message + assistant response
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"


def test_send_message_preserves_history():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="Response 1")
    ]

    history = [
        {"role": "user", "content": "First message"},
        {"role": "assistant", "content": "First response"},
    ]
    result = send_message(mock_client, "system prompt", history, "Second message", stream=False)

    assert result == "Response 1"
    assert len(history) == 4
    call_args = mock_client.messages.create.call_args
    assert len(call_args.kwargs["messages"]) == 4


def test_send_message_passes_system_prompt():
    mock_client = MagicMock()
    mock_client.messages.create.return_value.content = [
        MagicMock(text="yo")
    ]

    history = []
    send_message(mock_client, "test system prompt", history, "hi", stream=False)

    call_args = mock_client.messages.create.call_args
    assert call_args.kwargs["system"] == "test system prompt"
