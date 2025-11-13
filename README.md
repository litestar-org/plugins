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

- **Get README**: Fetch README files for all plugins

```sh
uv run get-readme
```

### Contribution

- If you feel a plugin is missing, please create a new [issue](https://github.com/litestar-org/plugin-registry/issues/new)
- If some data is outdated please directly open a pull request

### Schema

Field Name                    | Required              | Description
------------------------------|----------------------|------------------------------------------
`key`                         | :white_check_mark:   | Unique identifier for the plugin
`name`                        | :white_check_mark:   | Name displayed on the website
`description`                 | :white_check_mark:   | Short description
`repo`                        | :white_check_mark:   | GitHub repository. Format is `org/name` or `org/name#main/path`
`pypi`                        | :white_check_mark:   | PyPi package name
`github`                      | :white_check_mark:   | GitHub URL
`website`                     | :white_check_mark:   | Website URL
`documentation`               | :white_check_mark:   | Link to the documentation
`category`                    | :white_check_mark:   | Plugin category from (TODO: Define a list of categories)
`type`                        | :white_check_mark:   | `official` (for litestar-org) or `3rd-party`
`maintainers`                 | :white_check_mark:   | List of maintainers each item has `name`, `github` and `avatar`
`compatibility`               | :white_check_mark:   | Plugins compatibility status. `litestar` field specifies semver of supported litestar version
`icon`                        | :grey_question:      | Icon of plugin from [./icons](./icons) directory
`stars`                       | :grey_question:      | GitHub repository star count (auto-populated)
`monthly_downloads`           | :grey_question:      | Monthly downloads from PyPI Stats (auto-populated)
`latest_version`              | :grey_question:      | Latest version from PyPI (auto-populated)
`created_at`                  | :grey_question:      | Plugin creation date from PyPI releases (auto-populated)
`updated_at`                  | :grey_question:      | Plugin last update date from PyPI releases (auto-populated)
`python_compatibility_raw`   | :grey_question:      | Raw Python version requirement string from PyPI (auto-populated)
`python_compatibility`       | :grey_question:      | Parsed Python compatibility object with `raw`, `specifier_set`, and `compatible` fields (auto-populated)
`changelog`                   | :grey_question:      | Changelog URL from PyPI project_urls (auto-populated)
`issues`                      | :grey_question:      | Issues/Bug tracker URL from PyPI project_urls (auto-populated)

> [!WARNING]
> Modifying the schema there needs to be done also in the litestar.dev website repository.