import json
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

from github_client import fetch_recent_repos, format_repos_for_prompt


MOCK_REPOS = [
    {
        "name": "KtulueChatBot",
        "description": "AI-powered personal chatbot",
        "language": "Python",
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "html_url": "https://github.com/Ktulue/KtulueChatBot",
    },
    {
        "name": "HypeControl",
        "description": "Twitch spending friction extension",
        "language": "JavaScript",
        "pushed_at": datetime.now(timezone.utc).isoformat(),
        "html_url": "https://github.com/Ktulue/HypeControl",
    },
    {
        "name": "old-abandoned-repo",
        "description": "Something from years ago",
        "language": "Ruby",
        "pushed_at": "2020-01-01T00:00:00Z",
        "html_url": "https://github.com/Ktulue/old-abandoned-repo",
    },
]


def test_fetch_recent_repos_filters_old_repos():
    with patch("github_client.httpx.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_REPOS
        mock_get.return_value.raise_for_status = lambda: None

        repos = fetch_recent_repos(months=6)

    assert len(repos) == 2
    names = [r["name"] for r in repos]
    assert "KtulueChatBot" in names
    assert "HypeControl" in names
    assert "old-abandoned-repo" not in names


def test_fetch_recent_repos_handles_api_failure():
    with patch("github_client.httpx.get") as mock_get:
        mock_get.side_effect = Exception("API down")

        repos = fetch_recent_repos()

    assert repos == []


def test_format_repos_for_prompt_with_repos():
    repos = [
        {
            "name": "KtulueChatBot",
            "description": "AI-powered personal chatbot",
            "language": "Python",
            "pushed_at": "2026-04-01T00:00:00Z",
        },
    ]
    result = format_repos_for_prompt(repos)
    assert "KtulueChatBot" in result
    assert "Python" in result
    assert "AI-powered personal chatbot" in result


def test_format_repos_for_prompt_empty():
    result = format_repos_for_prompt([])
    assert isinstance(result, str)
    assert len(result) > 0  # Should return a fallback message
