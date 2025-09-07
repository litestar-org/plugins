from typing import Dict, List, Optional, Literal
import msgspec
from src.categories import Category
from datetime import datetime

class PluginCompatibility(msgspec.Struct):
    litestar: str


class MaintainerInfo(msgspec.Struct):
    name: str
    github: str
    avatar: str

class PythonCompatibility(msgspec.Struct):
    raw: str
    specifier_set: str
    compatible: List[str]

ModuleType = Literal["official", "3rd-party"]


class PluginInfo(msgspec.Struct):
    key: str
    name: str
    description: str
    pypi: str
    repo: str
    github: str
    website: str
    documentation: str
    category: Category
    type: ModuleType
    maintainers: List[MaintainerInfo]
    compatibility: PluginCompatibility
    icon: str | None = None
    # Fetched at sync from github
    stars: Optional[int] = 0
    # Fetched from pypistats
    monthly_downloads: Optional[int] = 0
    # Fetched at sync from pypi
    latest_version: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    python_compatibility_raw: Optional[str] = None
    python_compatibility: Optional[PythonCompatibility] = None
    changelog: Optional[str] = None
    issues: Optional[str] = None