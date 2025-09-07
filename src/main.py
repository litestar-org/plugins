import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
import glob
import msgspec
import structlog
from datetime import datetime

from src.types import PluginInfo
from src.utils import fetch_pypi, fetch_pypistats, get_github_stars_auth, parse_requires_python
from src.constants import (
    PLUGINS_DIR,
    DIST_DIR,
    GENERATED_PLUGIN_DIST_FILE,
    ROOT_DIR,
    GENERATED_FILENAME,
    DEFAULT_PLUGIN_ICON,
)

logger = structlog.get_logger()


async def sync(key: str) -> PluginInfo:
    """Sync plugin information from various sources."""
    plugin = await get_plugin(key)

    if not plugin:
        await logger.aerror("Plugin not found", plugin_key=key)
        raise ValueError(f"Plugin with key {key} not found")

    # Validate and assign icon
    if plugin.icon:
        icon_file = ROOT_DIR / "icons" / plugin.icon
        if not icon_file.exists():
            await logger.aerror(f"Icon {plugin.icon} does not exist for {plugin.key}")
            raise ValueError(f"Icon {plugin.icon} does not exist for {plugin.key}")
    else:
        # Assign default icon if none provided
        plugin.icon = DEFAULT_PLUGIN_ICON
        await logger.awarning(
            f"Assigned default icon to plugin {plugin.name}", icon=plugin.icon
        )

    # Retrieves github starts
    if plugin.repo:
        stars = await get_github_stars_auth(plugin.repo)
        if stars is not None:
            plugin.stars = stars

    # Retrieves data from PyPI
    if plugin.pypi:
        pypi_data = await fetch_pypi(plugin.pypi)
        if pypi_data:
            info = pypi_data.get("info", {})
            releases = pypi_data.get("releases", {})
            
            # Get version
            plugin.latest_version = info.get("version")
            
            # Get python compatibility
            plugin.python_compatibility_raw = info.get("requires_python")
            plugin.python_compatibility = parse_requires_python(plugin.python_compatibility_raw)

            # Get changelog and issues from project_urls
            project_urls = info.get("project_urls", {})
            if project_urls:
                plugin.changelog = project_urls.get("Changelog")
                plugin.issues = project_urls.get("Issue")
            
            # Get created_at and updated_at from releases
            if releases:
                upload_times = []
                for version_releases in releases.values():
                    for release in version_releases:
                        if upload_time := release.get("upload_time"):
                            try:
                                upload_times.append(datetime.fromisoformat(upload_time.replace('Z', '+00:00')))
                            except (ValueError, AttributeError):
                                continue
                
                if upload_times:
                    upload_times.sort()
                    plugin.created_at = upload_times[0]  # Oldest
                    plugin.updated_at = upload_times[-1]  # Newest
        
    # Retrieves data from PyPI Stats
    if plugin.pypi:
        pypistats_data = await fetch_pypistats(plugin.pypi)
        if pypistats_data:
            data = pypistats_data.get("data", {})
            if data:
                plugin.monthly_downloads = data.get("last_month")

    # Convert to dict to manipulate fields
    plugin_dict = msgspec.to_builtins(plugin)

    # Reconstruct module from cleaned dict
    plugin = msgspec.convert(plugin_dict, PluginInfo)

    # Write plugin
    await write_plugin(plugin)

    return plugin


async def get_plugin(key: str) -> PluginInfo | None:
    """Get plugin configuration."""

    # Load existing configuration if it exists
    file_path = PLUGINS_DIR / f"{key}.yml"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return msgspec.convert(data, PluginInfo)

    return None


async def write_plugin(plugin: PluginInfo) -> None:
    """Write plugin configuration to YAML file."""
    file_path = PLUGINS_DIR / f"{plugin.key}.yml"

    # Convert to dict for YAML serialization
    plugin_dict = msgspec.to_builtins(plugin)

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(plugin_dict, f, default_flow_style=False, sort_keys=False)


async def read_plugins() -> List[PluginInfo]:
    """Read all plugin configurations."""
    pattern = str(PLUGINS_DIR / "*.yml")
    files = glob.glob(pattern)

    names = [
        Path(f).stem
        for f in files
        if Path(f).stem  # Filter out empty names
    ]

    tasks = [get_plugin(name) for name in names]
    plugins = await asyncio.gather(*tasks)

    return [p for p in plugins if p.name]


async def sync_all() -> Dict[str, Any]:
    """Sync all plugins with rate limiting."""
    plugins = await read_plugins()
    success: bool = True

    # Rate limiting using semaphore (equivalent to pLimit(10))
    semaphore = asyncio.Semaphore(10)

    async def sync_with_limit(plugin: PluginInfo) -> Optional[PluginInfo]:
        async with semaphore:
            try:
                await logger.ainfo(f"Syncing plugin {plugin.key}")
                return await sync(plugin.key)
            except Exception as err:
                await logger.aerror(
                    f"Error syncing plugin {plugin.key}", error=str(err)
                )
                return None

    tasks = [sync_with_limit(plugin) for plugin in plugins]
    updated_plugins = await asyncio.gather(*tasks, return_exceptions=True)

    return {"count": len(updated_plugins), "success": success}


async def build() -> None:
    """Build the final modules.json file."""
    await logger.ainfo("Build process started")

    plugins = await read_plugins()

    # Ensure dist directory exists
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # Convert plugins to dictionaries for JSON serialization
    plugins_data = [msgspec.to_builtins(plugin) for plugin in plugins]

    # Write to JSON file
    with open(GENERATED_PLUGIN_DIST_FILE, "w", encoding="utf-8") as f:
        json.dump(plugins_data, f, indent=2, ensure_ascii=False)

    await logger.ainfo(
        f"Build process completed successfully. Check out {GENERATED_FILENAME} file"
    )


def build_cli() -> None:
    """CLI wrapper for the build command."""
    asyncio.run(build())


def sync_all_cli() -> None:
    """CLI wrapper for the sync_all command."""
    logger.info("Starting sync all")
    result = asyncio.run(sync_all())
    logger.info("Sync all completed", count=result["count"], success=result["success"])
