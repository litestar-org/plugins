# Litestar plugins

Home for plugins for Litestar

## Plugins Database

Metadata of litestar plugins are maintained in [yml](https://en.wikipedia.org/wiki/YAML) files inside [./plugins](./plugins) directory and automatically synced from upstream to fetch latest information.

### Add/Update a plugin

Create a PR:
- Copy the [example.yml](example.yml) file.
- Image must be svg or png

### Commands

- **Sync**: Update plugin metadata from upstream sources

```sh
uv run sync
```

- **Build**: Generate the plugins file

```sh
uv run build
```

### Contribution

- If you feel a plugin is missing, please create a new [issue](https://github.com/litestar-org/plugins/issues/new)
- If some data is outdated please directly open a pull request

### Schema

Field Name                    | Description
------------------------------|------------------------------------------
`key`                         | Unique identifier for the plugin
`name`                        | Name displayed on the website
`description`                 | Short description
`repo`                        | GitHub repository. Format is `org/name` or `org/name#main/path`
`pypi`                        | PyPi package name
`icon`                        | Icon of plugin from [./icons](./icons) directory
`github`                      | GitHub URL
`website`                     | Website URL
`documentation`               | Link to the documentation
`category`                    | Plugin category from (TODO: Define a list of categories)
`type`                        | `official` (for litestar-org) or `3rd-party`
`maintainers`                 | List of maintainers each item has `name`, `github` and `avatar`
`compatibility`               | Plugins compatibility status. `litestar` field specifies semver of supported litestar version
`stars`                       | GitHub repository star count (auto-populated)
`monthly_downloads`           | Monthly downloads from PyPI Stats (auto-populated)
`latest_version`              | Latest version from PyPI (auto-populated)
`created_at`                  | Plugin creation date from PyPI releases (auto-populated)
`updated_at`                  | Plugin last update date from PyPI releases (auto-populated)
`python_compatibility_raw`   | Raw Python version requirement string from PyPI (auto-populated)
`python_compatibility`       | Parsed Python compatibility object with `raw`, `specifier_set`, and `compatible` fields (auto-populated)
`changelog`                   | Changelog URL from PyPI project_urls (auto-populated)
`issues`                      | Issues/Bug tracker URL from PyPI project_urls (auto-populated)

> [!WARNING]
> Modifying the schema there needs to be done also in the litestar.dev website repository.