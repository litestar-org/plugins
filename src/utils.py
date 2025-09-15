import os
import niquests

from typing import Any, Dict, Optional
from packaging.specifiers import SpecifierSet
from src.types import PythonCompatibility


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


async def get_github_readme(repo: str) -> Optional[str]:
    """Get README content from GitHub repository using GitHub API."""
    url = f"https://api.github.com/repos/{repo}/readme"
    headers = {"Accept": "application/vnd.github.raw"}

    # Add auth header if token is available
    if github_token := os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {github_token}"

    try:
        response: niquests.Response = await niquests.aget(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching README for {repo}: {e}")
        return None


def parse_requires_python(requires_python: str) -> PythonCompatibility:
    """Parse using packaging library for proper version handling."""
    if not requires_python:
        return PythonCompatibility(raw="", specifier_set="", compatible=[])

    try:
        spec_set = SpecifierSet(requires_python)

        # Generate list of compatible Python versions
        compatible_versions: list[str] = []
        # Test common Python versions
        python_versions: list[str] = [
            "3.9",
            "3.10",
            "3.11",
            "3.12",
            "3.13",
            "3.14",
        ]

        for version in python_versions:
            if spec_set.contains(version):
                compatible_versions.append(version)

        return PythonCompatibility(
            raw=requires_python,
            specifier_set=str(spec_set),
            compatible=compatible_versions,
        )
    except Exception:
        return PythonCompatibility(
            raw=requires_python, specifier_set="Invalid format", compatible=[]
        )
