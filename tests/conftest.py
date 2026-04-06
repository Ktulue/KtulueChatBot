"""Shared pytest fixtures for the KtulueChatBot test suite."""
import os
from unittest.mock import MagicMock

import pytest

# Set a fake API key BEFORE any test imports anthropic, so client construction
# inside web.app's lifespan would not fail if it ran. The lifespan does not run
# under TestClient unless used as a context manager, but this guards against
# accidental real-client construction in any other code path.
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-real")


@pytest.fixture
def mock_anthropic_client():
    """A MagicMock standing in for an anthropic.Anthropic() instance."""
    return MagicMock()


@pytest.fixture
def web_app(mock_anthropic_client):
    """Import and configure the FastAPI app with mocked startup state.

    The TestClient is NOT used as a context manager in tests, so the lifespan
    never runs. We populate web.app.state directly with mocks to bypass startup.
    """
    from web import app as web_app_module

    web_app_module.state["system_prompt"] = "MOCK SYSTEM PROMPT"
    web_app_module.state["client"] = mock_anthropic_client
    web_app_module.sessions.clear()

    yield web_app_module.app

    web_app_module.sessions.clear()


@pytest.fixture
def web_client(web_app):
    """A FastAPI TestClient bound to the configured web app."""
    from fastapi.testclient import TestClient

    client = TestClient(web_app)
    yield client
    client.close()
