# Code Editor

Code Editor is a Home Assistant app that provides a browser-based Visual Studio
Code experience for editing your Home Assistant configuration. It is powered by
[code-server](https://github.com/coder/code-server) and runs inside the Home
Assistant frontend through ingress.

![Code Editor in the Home Assistant frontend](images/screenshot.png)

## Features

- Browser-based code editing inside Home Assistant.
- Home Assistant YAML language support and schema validation.
- ESPHome, YAML, Jinja, Python, Ruff, Prettier, and icon tooling bundled in the
  image.
- Home Assistant API access through Supervisor-provided environment variables.
- Persistent editor settings, extensions, terminal history, and Git config.
- Sensible defaults for Home Assistant configuration folders, generated files,
  database files, and frontend assets.

## Installation

This repository contains a Home Assistant Supervisor app. Install it by adding
this repository URL to the Home Assistant app store as a custom repository, then
installing **Code Editor** from the app list.

This is not a HACS integration. HACS manages custom integrations, frontend
cards, themes, and similar resources; Supervisor apps are installed from the
Home Assistant app store.

## Documentation

Full configuration and usage notes are in [vscode/DOCS.md](vscode/DOCS.md).

## Versioning

The app version is aligned with the embedded Visual Studio Code version when the
runtime changes. This release uses VS Code `1.118.0` through code-server
`v4.118.0`.

Packaging-only fixes can still use normal patch increments on the same version
train when needed.

## Support

Open an issue in this repository for problems with this app. When reporting an
issue, include the app version, Home Assistant OS version, Home Assistant Core
version, Supervisor version, architecture, and the app log.

## Credits

This app is based on the original Studio Code Server project by Franck Nijhof
and contributors.

## License

MIT License. See [LICENSE.md](LICENSE.md).
