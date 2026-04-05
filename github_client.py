from datetime import datetime, timezone, timedelta

import httpx

GITHUB_USER = "Ktulue"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USER}/repos"


def fetch_recent_repos(months: int = 6) -> list[dict]:
    """Fetch public repos for Ktulue with activity in the last N months."""
    try:
        response = httpx.get(
            GITHUB_API_URL,
            params={"type": "public", "sort": "pushed", "per_page": 30},
            timeout=10,
        )
        response.raise_for_status()
    except Exception:
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)
    repos = []
    for repo in response.json():
        pushed_at = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
        if pushed_at >= cutoff:
            repos.append(
                {
                    "name": repo["name"],
                    "description": repo.get("description") or "No description",
                    "language": repo.get("language") or "Unknown",
                    "pushed_at": repo["pushed_at"],
                }
            )
    return repos


def format_repos_for_prompt(repos: list[dict]) -> str:
    """Format repo list into a string for the system prompt."""
    if not repos:
        return "GitHub data is currently unavailable. Refer to project knowledge files for project info."

    lines = ["Recently active public repositories on GitHub:"]
    for repo in repos:
        lines.append(f"- **{repo['name']}** ({repo['language']}): {repo['description']}")
    return "\n".join(lines)
