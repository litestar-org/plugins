from pathlib import Path

# Path operations
ROOT_DIR: Path = Path(__file__).parent.parent.resolve()
PLUGINS_DIR: Path = ROOT_DIR.joinpath("plugins")
READMES_DIR: Path = ROOT_DIR.joinpath("readmes")
DIST_DIR: Path = ROOT_DIR
GENERATED_FILENAME = "plugins.yml"
GENERATED_PLUGIN_DIST_FILE: Path = DIST_DIR.joinpath(GENERATED_FILENAME)

# Default plugin icon
DEFAULT_PLUGIN_ICON = "_default_icon.svg"
