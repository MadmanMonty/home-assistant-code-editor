# Code Editor

Code Editor lets you edit your Home Assistant configuration files directly from
Home Assistant.

## Configuration

Most users can leave the configuration as-is. By default, Code Editor opens your
Home Assistant configuration folder, uses the normal log level, and does not run
any extra startup actions.

However, if you want to make lower level changes, these configuration items are available. Save the change and restart Code Editor after making changes.

### `log_level`

Controls how much detail appears in the **Log** tab.

The default value is `info`, which is right for normal use. If you are trying to
understand a problem, choose `debug` for more detail. Use `trace` only when very
detailed logs are needed.

Available choices:

- `trace`: Show the most detailed logs.
- `debug`: Show extra troubleshooting details.
- `info`: Show normal startup and activity messages.
- `notice`: Show notable events.
- `warning`: Show warnings that may need attention.
- `error`: Show errors.
- `fatal`: Show errors that stop Code Editor from working.

### `config_path`

Controls the folder Code Editor opens when it starts.

The default value is your main Home Assistant configuration folder:

```text
/config
```

Change this only if you want Code Editor to open a different folder under your
Home Assistant configuration, such as:

```text
/config/custom-folder
```

### `packages`

Adds extra command-line tools when Code Editor starts.

Most users should leave this empty. Add packages only if you know the package
name and need that tool inside Code Editor's terminal.

Example:

```yaml
packages:
  - mariadb-client
```

Adding packages can make Code Editor take longer to start.

### `init_commands`

Runs commands when Code Editor starts.

Most users should leave this empty. This is useful only for advanced personal
setup tasks that you want to happen every time Code Editor starts.

Example:

```yaml
init_commands:
  - ls -la /config
```

If a command fails, Code Editor may not start correctly.

## Resetting Editor Settings

Code Editor includes default editor settings for Home Assistant files. Once you
change those settings, your preferences are kept during updates.

To return to the default Code Editor settings:

1. Open Code Editor.
2. Open a new terminal.
3. Run `reset-settings`.
4. Restart Code Editor.
