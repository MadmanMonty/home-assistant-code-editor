# Code Editor

Code Editor lets you edit your Home Assistant configuration files directly from
Home Assistant.

![Code Editor in the Home Assistant frontend](assets/screenshot.png)

## Why use Code Editor?

- Edit Home Assistant configuration files from the same place you manage your
  home.
- Get helpful suggestions while writing automations, scripts, sensors, scenes,
  and dashboards.
- Catch common YAML and formatting problems before restarting Home Assistant.
- Work with ESPHome, templates, icons, Python files, and logs in one editor.
- Keep your editor preferences between updates.

## Installation

[![Add repository to my Home Assistant][repository-badge]][repository-url]

After adding the repository:

1. Open **Settings** in Home Assistant.
2. Go to **Apps**.
3. Select **Install app**.
4. Search for **Code Editor**.
5. Install and start the app.
6. Open **Code Editor** from the Home Assistant sidebar.

If the button does not work, add this repository manually:

```text
https://github.com/gollyjer/addon-vscode
```

## What the included extensions do

Code Editor includes extensions chosen for editing Home Assistant files:

- **Home Assistant Config Helper** adds Home Assistant-aware suggestions and
  validation while editing YAML configuration.
- **YAML** helps find indentation, spacing, and structure problems in YAML files.
- **ESPHome** makes ESPHome device configuration easier to read and edit.
- **File Git History** shows the git commit history for the file you are
  editing, so you can see how an automation or configuration changed over
  time without leaving the editor.
- **Jinja** improves editing for Home Assistant templates used in automations,
  template sensors, notifications, and dashboards.
- **Material Design Icons Intellisense** helps you find and insert `mdi:` icons
  used throughout Home Assistant.
- **Prettier** formats supported files so configuration stays consistent and easy
  to scan.
- **Python**, **Pylance**, and **Ruff** help when editing Python files used by
  advanced Home Assistant setups.
- **Log File Highlighter** makes Home Assistant logs easier to read when you need
  to troubleshoot a problem.
- **vscode-icons** adds file and folder icons so configuration files are easier to
  recognize at a glance.

## More help

More configuration and usage notes are available in
[code-editor/DOCS.md](code-editor/DOCS.md).

If something is not working, please
[open an issue](https://github.com/gollyjer/addon-vscode/issues).

## Credits

This app is based on the original Studio Code Server project by Franck Nijhof
and contributors.

## License

MIT License. See [LICENSE.md](LICENSE.md).

[repository-badge]: https://img.shields.io/badge/Add_repository_to_my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fgollyjer%2Faddon-vscode
