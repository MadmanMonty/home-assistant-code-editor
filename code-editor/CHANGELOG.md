# Changelog

This changelog starts at fork point
`776ef9119524ff489345a6a60e13333264e67b1c` from December 30, 2025 and
summarizes the Code Editor modernization through
`a087e51e9a8b8bf72a238d881f52b89bf899770d` from May 12, 2026.

## 1.118.0 - 2026-05-12

### Modernized Editor Stack

- Updated `code-server` from `v4.107.0` to `v4.118.0`, bringing the embedded
  Code editor from `1.107.0` to `1.118.0`.
- Updated the Code Editor app version to `1.118.0` to track the current editor
  stack.
- Updated the Home Assistant CLI from `4.45.0` to `5.1.0`.
- Updated the base image from `ghcr.io/hassio-addons/debian-base:9.1.0` to
  `ghcr.io/hassio-addons/debian-base:9.3.0`.
- Refreshed pinned system packages including `locales`, `openssh-client`,
  `openssl`, and `zsh`.
- Updated the bundled ESPHome Python tooling from `2025.12.3` to `2026.4.5`.

### Rebranded and Simplified Packaging

- Renamed the app from `Studio Code Server` to `Code Editor`.
- Moved the app source tree from `vscode/` to `code-editor/`.
- Changed the Home Assistant slug from `vscode` to `code_editor`.
- Updated Home Assistant metadata, Docker labels, OCI labels, documentation,
  service script headers, icon, logo, and screenshot assets for the new Code
  Editor identity.
- Changed Home Assistant metadata from an add-on style service to an app style
  package, including `startup: application` and `io.hass.type="app"`.
- Removed the deprecated `build.yaml` file and now pins the base image directly
  in the `Dockerfile`.
- Replaced inherited generic build labels with explicit Code Editor labels,
  maintainer details, and repository/documentation URLs.

### Faster Startup and Smaller Runtime Surface

- Removed MariaDB and MQTT client packages from the default image. Users who
  still need those tools can install them with the `packages` option.
- Removed Mosquitto and MySQL initialization scripts and their wanted service
  declarations.
- Removed broad default Home Assistant mounts for `addons`, `all_addon_configs`,
  `backup`, `media`, `share`, and `ssl`; the app now maps the Home Assistant
  configuration folder at `/config` by default.
- Removed the unused `uart` option.
- Removed automatic home-directory links for broad Home Assistant folders while
  keeping compatibility links for `/config` and `/homeassistant`.
- Removed the redundant `yamllint` Python dependency and `libarchive-tools`
  package.
- Continued to persist SSH settings, Git settings, zsh history, user-installed
  packages, and configured startup commands under `/data`.

### Extension Handling

- Changed build-time extension handling to download validated VSIX packages into
  `/usr/local/share/code-server/vsix`.
- Changed startup extension handling to install bundled VSIX packages through
  `code-server --install-extension` into `/data/code-editor/extensions`.
- Avoids reinstalling bundled extensions when the requested version is already
  present.
- Clears stale extension scanner files, including `.obsolete` and
  `extensions.json`, from persistent extension storage on startup.
- Added warnings for missing or failed bundled extension installs so extension
  state is easier to diagnose.
- Added `extensions.supportNodeGlobalNavigator` for newer extension runtime
  behavior.
- Disabled extension auto-check and auto-update by default so the Home Assistant
  editor environment stays deterministic across restarts.

### Bundled Extension Updates

- Updated Log File Highlighter from `3.4.5` to `3.5.1`.
- Updated Prettier from `11.0.2` to `12.4.0`.
- Updated ESPHome from `2025.4.2` to `2026.4.0`.
- Updated Red Hat YAML from `1.11.10112022` to `1.24.2026050908`.
- Kept Home Assistant Config Helper and Material Design Icons Intellisense.
- Added Python, Debugpy, Pylance, Ruff, Jinja, and vscode-icons for a more
  complete Home Assistant-focused editing environment.
- Removed Indent Rainbow and Error Lens from the bundled defaults.
- Removed Copilot Chat from the extension list because it is already included by
  code-server.

### Home Assistant Editor Defaults

- Default workspace remains `/config`, with a guard that prevents using `/` as
  the workspace because indexing the full container filesystem is expensive.
- Added explicit default `log_level: info` and required schema values for
  `log_level` and `config_path`.
- Expanded watcher, search, and file excludes for common Home Assistant generated
  or noisy paths, including `tts`, `www/community`, and `www/custom_ui`.
- Set the default theme to `Default Dark Modern`, moved the activity bar to the
  top, disabled the startup editor, and enabled the `vscode-icons` icon theme.
- Updated the integrated terminal configuration to use the modern zsh profile
  settings.
- Added defaults for line endings, final newlines, trimming trailing whitespace,
  the Python interpreter path, Ruff behavior, and telemetry opt-outs.
- Preserved Home Assistant YAML associations, YAML custom tags, ESPHome local
  validation, and format-on-save behavior for Home Assistant YAML files.

### Documentation and Repository Cleanup

- Rewrote the README for the new Code Editor name, Home Assistant app install
  flow, included extension list, and support links.
- Reworked `DOCS.md` into a shorter user-facing configuration guide.
- Added `translations/en.yaml` for app metadata and options.
- Removed inherited GitHub community, workflow, Renovate, Markdown lint, and
  YAML lint configuration files that no longer applied to this fork.
- Updated license attribution and year.

### Migration Notes

- The slug changed from `vscode` to `code_editor`, so Home Assistant may treat
  this as a separate app from the original Studio Code Server add-on.
- The default mapped workspace is now focused on `/config`. Add any extra
  command-line tools you need through the `packages` option.
- User editor settings persist in `/data/code-editor`. Default
  settings are refreshed only when the stored settings still match a known
  previous default.

### References

- Baseline fork commit:
  `776ef9119524ff489345a6a60e13333264e67b1c`
- Current summarized commit:
  `a087e51e9a8b8bf72a238d881f52b89bf899770d`
- code-server `v4.118.0` release:
  https://github.com/coder/code-server/releases/tag/v4.118.0
