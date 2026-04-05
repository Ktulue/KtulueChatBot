from unittest.mock import patch

from personality import build_system_prompt, load_knowledge_file


def test_load_knowledge_file_returns_content():
    content = load_knowledge_file("bio.md")
    assert "Josh" in content
    assert "Ktulue" in content


def test_load_knowledge_file_missing_file():
    content = load_knowledge_file("nonexistent.md")
    assert content == ""


def test_build_system_prompt_contains_identity():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "KtulueBot" in prompt or "Ktulue" in prompt
    assert "Josh" in prompt


def test_build_system_prompt_contains_voice_directives():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "sarcasm" in prompt.lower() or "humor" in prompt.lower()
    assert "Water Father" in prompt


def test_build_system_prompt_contains_guardrails():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "NEVER" in prompt
    assert "invent facts" in prompt.lower() or "hallucinate" in prompt.lower() or "don't know" in prompt.lower()


def test_build_system_prompt_contains_all_knowledge_sections():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    # Check that all knowledge files are represented
    assert "Wicket" in prompt  # from bio.md
    assert "Software Saturdays" in prompt  # from streaming.md
    assert "Hype Control" in prompt  # from projects.md
    assert "AI" in prompt  # from tech.md
    assert "SSN" in prompt or "personal details" in prompt.lower()  # from boundaries.md


def test_build_system_prompt_contains_deflection_examples():
    with patch("personality.format_repos_for_prompt", return_value="No repos"):
        prompt = build_system_prompt()
    assert "deflect" in prompt.lower() or "redirect" in prompt.lower()


def test_build_system_prompt_includes_github_data():
    mock_github = "Recently active: KtulueChatBot (Python)"
    with patch("personality.format_repos_for_prompt", return_value=mock_github):
        prompt = build_system_prompt()
    assert "KtulueChatBot (Python)" in prompt
