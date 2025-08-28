# Litestar plugins

Home for plugins for Litestar

## Plugins Database

Metadata of litestar plugins are maintained in [yml](https://en.wikipedia.org/wiki/YAML) files inside [./plugins](./plugins) directory and automatically synced from upstream to fetch latest information.

### Add/Update a plugin

Create a PR:
- Copy the [example.yml](example.yml) file.
- Image must be svg or png

### Contribution

- If you feel a plugin is missing, please create a new [issue](https://github.com/litestar-org/plugins/issues/new)
- If some data is outdated please directly open a pull request

### Schema

Field Name      | Description
----------------|--------------
`name`          | Name displayed on the website
`description`   | Short description
`repo`          | GitHub repository. Format is `org/name` or `org/name#main/path`
`pypi`          | PyPi package name
`icon`          | Icon of plugin from [./icons](./icons) directory
`github`        | GitHub URL
`website`       | Website URL
`documentation` | Link to the documentation
`category`      | Plugin category from [./lib/categories.ts](./lib/categories.ts)
`type`          | `official` (for litestar-org) or `3rd-party`
`maintainers`   | List of maintainers each item has `name`, `github` and `avatar`
`compatibility` | Plugins compatibility status. `litestar` field specifies semver of supported litestar version.