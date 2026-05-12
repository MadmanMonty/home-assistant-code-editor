# Code Editor

Code Editor is a Home Assistant app that runs
[code-server](https://github.com/coder/code-server), giving you a Visual Studio
Code experience directly in the Home Assistant frontend.

The app is preconfigured for Home Assistant work: YAML files open with Home
Assistant language support, ESPHome files use the ESPHome language mode, common
generated files are hidden from search, and useful editor extensions are bundled
with the image.

## Installation

1. Add this repository URL to the Home Assistant app store as a custom
   repository.
2. Install **Code Editor** from the app list.
3. Start **Code Editor**.
4. Check the app logs to confirm startup completed successfully.
5. Open the web UI from Home Assistant.

## Configuration

Restart the app after changing its configuration.

Example app configuration:

```yaml
log_level: info
config_path: /share/my_path
packages:
  - mariadb-client
init_commands:
  - ls -la
```

This is only an example. Adjust it for your own environment.

### Option: `log_level`

The `log_level` option controls app log verbosity. Possible values are:

- `trace`: Show every detail, including internal function calls.
- `debug`: Show detailed debug information.
- `info`: Show normal startup and runtime events.
- `notice`: Show notable events.
- `warning`: Show exceptional occurrences that are not fatal errors.
- `error`: Show runtime errors that do not require immediate action.
- `fatal`: Show errors that prevent the app from being usable.

The default is `info`, which is recommended unless you are troubleshooting.

### Option: `config_path`

The `config_path` option controls the folder opened by default in Code Editor.
When omitted, the app opens `/config`.

Use a specific folder such as `/config`, `/share/myconfig`, or another mapped
path. Do not use `/` as the workspace; the app rejects it because indexing the
entire container filesystem causes severe performance problems.

### Option: `packages`

The `packages` option installs additional Debian packages into the app's shell
environment on startup.

Adding packages increases startup time. Prefer baking common tools into the
image when you need them consistently.

### Option: `init_commands`

The `init_commands` option runs one or more shell commands each time the app
starts. Use it for small environment tweaks that are specific to your Home
Assistant instance.

## Bundled Extensions

The app bundles a curated set of extensions for Home Assistant configuration and
development work:

- ESPHome
- Home Assistant Config Helper
- Material Design Icons Intellisense
- Prettier
- Python
- Pylance
- Ruff
- YAML
- Jinja
- vscode-icons
- Log File Highlighter

code-server currently includes GitHub Copilot Chat as a built-in extension. It
is not installed separately by this app.

## Resetting Editor Settings

The app installs optimized default settings for Home Assistant. Once you change
your user settings, the app stops replacing them so your preferences are not
overwritten.

To reset to the app defaults:

1. Open Code Editor.
2. Open a new terminal.
3. Run `reset-settings`.
4. Restart the app.

## Known Issues and Limitations

- The app supports `amd64` and `aarch64` only.
- ARM devices are supported, but the editor can be heavy on small systems. A
  device with less than 4 GB of memory is not recommended.
- Do not use `/` as the workspace. Use `/config` or another specific mapped
  folder.
- If VS Code reports that it cannot watch file changes in a large workspace,
  dismiss the warning or narrow your workspace to a smaller folder.
- Some internal Home Assistant and Supervisor APIs still use `addon` naming even
  though the Home Assistant UI now calls these apps. The app configuration keeps
  those internal keys where Supervisor requires them.

## Versioning

The app version is aligned with the embedded Visual Studio Code version when the
runtime changes. This release uses VS Code `1.118.0` through code-server
`v4.118.0`.

Packaging-only fixes can still use normal patch increments on the same version
train when needed.

## Support

When asking for help, include:

- Code Editor version
- Home Assistant OS version
- Home Assistant Core version
- Home Assistant Supervisor version
- Architecture
- Relevant app logs

Open an issue in this repository for app-specific problems.

## Credits

This app is based on the original Studio Code Server project by Franck Nijhof
and contributors.

## License

MIT License. See the repository license file.
