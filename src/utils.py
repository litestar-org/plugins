import os
from typing import Any, Dict, Optional
import niquests

# Create a session for better performance with multiple requests


async def fetch_pypi(name: str) -> Dict[str, Any]:
    """Fetch package info from PyPI registry."""
    url: str = f"https://pypi.org/pypi/{name}/json"
    response: niquests.Response = await niquests.aget(url)
    response.raise_for_status()
    return response.json()


async def get_github_stars_auth(repo: str) -> Optional[int]:
    """Get star count with GitHub token authentication."""
    url = f"https://api.github.com/repos/{repo}"
    headers = {}

    # Add auth header if token is available
    if github_token := os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {github_token}"

    try:
        response: niquests.Response = await niquests.aget(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("stargazers_count")
    except Exception as e:
        print(f"Error fetching stars for {repo}: {e}")
        return None

async def fetch_pypistats(name: str) -> Dict[str, Any]:
    """Fetch package info from PyPi Stats."""
    url: str = f"https://pypistats.org/api/packages/{name}/recent"
    response: niquests.Response = await niquests.aget(url)
    response.raise_for_status()
    return response.json()
